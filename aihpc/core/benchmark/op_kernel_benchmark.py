'''
Author       : Thinksky5124
Date         : 2024-03-29 20:18:21
LastEditors  : Thinksky5124
LastEditTime : 2024-04-22 18:47:43
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/benchmark/op_kernel_benchmark.py
'''
from abc import ABCMeta
import time
import torch
import functools
from typing import Any, Dict, List, Callable

from .base_benchmark import BaseBenchmark
from ..dispatcher import get_backend_type, BackendType, Dispatcher, get_torch_map_device
from ..utils import ObjectRegister

@ObjectRegister.register('benchmark')
class OpKernelBenchmark(BaseBenchmark):
    backend_type: BackendType
    def __init__(self,
                 op_name: str,
                 backends: str,
                 data_provider: Dict[str, Any],
                 x_names: str,
                 x_vals: List[Any],
                 quantiles: List[float] = None,
                 warmup: int = 25,
                 repeat_num: int = 100,
                 fast_flush: bool = True,
                 return_mode: str = "mean") -> None:
        self.op_name = op_name
        self.backend_names = [backend_name for backend_name in backends]
        self.backend_types = [get_backend_type(backend_name) for backend_name in backends]
        super().__init__(data_provider, x_names, x_vals, warmup,
                         repeat_num, return_mode)
        self.fast_flush = fast_flush
        self.quantiles = quantiles

    def _run(self,
            kernel_fn: callable,
            fn_kwargs: Dict[str, Any],
            tensor_gen_kwargs: Dict[str, Any],
            grad_to_none: torch.Tensor = None):
        """
        Benchmark the runtime of the provided function. By default, return the median runtime of :code:`fn` along with
        the 20-th and 80-th performance percentile.

        :param fn: Function to benchmark
        :type fn: Callable
        :param warmup: Warmup time (in ms)
        :type warmuargs, **kwargs, int
        :param rep: Repetition time (in ms)
        :type rep: int
        :param grad_to_none: Reset the gradient of the provided tensor to None
        :type grad_to_none: torch.tensor, optional
        :param quantiles: Performance percentile to return in addition to the median.
        :type quantiles: list[float]
        :param fast_flush: Use faster kernel to flush L2 between measurements
        :type fast_flush: bool
        """
        ## construct the function
        x_kwargs = {}
        x_kwargs.update(fn_kwargs)
        x_kwargs.update(tensor_gen_kwargs)
        args, kwargs = self.get_function_input(x_kwargs=x_kwargs)
        fn = functools.partial(self.function, fn=kernel_fn, args=args, kwargs=kwargs)

        if tensor_gen_kwargs['map_device'] == torch.device('cuda'):
            return self._run_cuda(fn, fn_kwargs, grad_to_none)
        elif tensor_gen_kwargs['map_device'] == torch.device('cpu'):
            return self._run_cpu(fn, fn_kwargs, grad_to_none)
        else:
            raise NotImplementedError(f"Unsupported device: {tensor_gen_kwargs['map_device']}")

    def _run_cuda(self,
                  fn: callable,
                  fn_kwargs: Dict[str, Any],
                  grad_to_none: torch.Tensor = None):
        fn()
        torch.cuda.synchronize()

        # We maintain a buffer of 256 MB that we clear
        # before each kernel call to make sure that the L2
        # doesn't contain any input data before the run
        if self.fast_flush:
            cache = torch.empty(int(256e6 // 4), dtype=torch.int, device='cuda')
        else:
            cache = torch.empty(int(256e6), dtype=torch.int8, device='cuda')

        # Estimate the runtime of the function
        start_event = torch.cuda.Event(enable_timing=True)
        end_event = torch.cuda.Event(enable_timing=True)
        start_event.record()
        for _ in range(5):
            cache.zero_()
            fn()

        end_event.record()
        torch.cuda.synchronize()
        estimate_ms = start_event.elapsed_time(end_event) / 5

        # compute number of warmup and repeat
        n_warmup = max(1, int(self.warmup / estimate_ms))
        n_repeat = max(1, int(self.repeat_num / estimate_ms))
        start_event = [torch.cuda.Event(enable_timing=True) for i in range(n_repeat)]
        end_event = [torch.cuda.Event(enable_timing=True) for i in range(n_repeat)]

        # Warm-up
        for _ in range(n_warmup):
            fn()

        # Benchmark
        for i in range(n_repeat):
            # we don't want `fn` to accumulate gradient values
            # if it contains a backward pass. So we clear the
            # provided gradients
            if grad_to_none is not None:
                for x in grad_to_none:
                    x.grad = None
            # we clear the L2 cache before each run
            cache.zero_()
            # record time of `fn`
            start_event[i].record()
            fn()
            end_event[i].record()
            
        # Record clocks
        torch.cuda.synchronize()
        times = torch.tensor([s.elapsed_time(e) for s, e in zip(start_event, end_event)], dtype=torch.float)
        
        if self.quantiles is not None:
            ret = torch.quantile(times, torch.tensor(self.quantiles, dtype=torch.float)).tolist()
            if len(ret) == 1:
                ret = ret[0]
            else:
                ms, min_ms, max_ms = ret
                return self.data_provider.gbps(ms, **fn_kwargs), self.data_provider.gbps(max_ms, **fn_kwargs), self.data_provider.gbps(min_ms, **fn_kwargs)
        else:
            ms, min_ms, max_ms = getattr(torch, self.return_mode)(times).item()
            return self.data_provider.gbps(ms, **fn_kwargs), self.data_provider.gbps(max_ms, **fn_kwargs), self.data_provider.gbps(min_ms, **fn_kwargs)
    
    def _run_cpu(self,
                  fn: callable,
                  fn_kwargs: Dict[str, Any],
                  grad_to_none: torch.Tensor = None):
        fn()
        torch.cpu.synchronize()

        # We maintain a buffer of 256 MB that we clear
        # before each kernel call to make sure that the L2
        # doesn't contain any input data before the run
        if self.fast_flush:
            cache = torch.empty(int(256e6 // 4), dtype=torch.int, device='cuda')
        else:
            cache = torch.empty(int(256e6), dtype=torch.int8, device='cuda')

        # Estimate the runtime of the function
        start_time = time.perf_counter()
        for _ in range(5):
            cache.zero_()
            fn()

        torch.cpu.synchronize()
        estimate_ms = ((time.perf_counter() - start_time) * 1000) / 5

        # compute number of warmup and repeat
        n_warmup = max(1, int(self.warmup / estimate_ms))
        n_repeat = max(1, int(self.repeat_num / estimate_ms))
        start_event = [None for i in range(n_repeat)]
        end_event = [None for i in range(n_repeat)]

        # Warm-up
        for _ in range(n_warmup):
            fn()

        # Benchmark
        for i in range(n_repeat):
            # we don't want `fn` to accumulate gradient values
            # if it contains a backward pass. So we clear the
            # provided gradients
            if grad_to_none is not None:
                for x in grad_to_none:
                    x.grad = None
            # we clear the L2 cache before each run
            cache.zero_()
            # record time of `fn`
            start_event[i] = time.perf_counter()
            fn()
            end_event[i] = time.perf_counter()
            
        # Record clocks
        torch.cpu.synchronize()
        times = torch.tensor([(e - s) * 1000 for s, e in zip(start_event, end_event)], dtype=torch.float)
        
        if self.quantiles is not None:
            ret = torch.quantile(times, torch.tensor(self.quantiles, dtype=torch.float)).tolist()
            if len(ret) == 1:
                ret = ret[0]
            else:
                ms, min_ms, max_ms = ret
                return self.data_provider.gbps(ms, **fn_kwargs), self.data_provider.gbps(max_ms, **fn_kwargs), self.data_provider.gbps(min_ms, **fn_kwargs)
        else:
            ms, min_ms, max_ms = getattr(torch, self.return_mode)(times).item()
            return self.data_provider.gbps(ms, **fn_kwargs), self.data_provider.gbps(max_ms, **fn_kwargs), self.data_provider.gbps(min_ms, **fn_kwargs)
        
    def register_callback_after_backend(self, fn: Callable[..., Any], position: str = 'after_backend') -> None:
        return super().register_callback(position, fn)
    
    def run(self):
        for x in self.x_vals:
            x_args = {x_name: x for x_name in self.x_names}
            for backend_type in self.backend_types:
                ret = self._run(kernel_fn = Dispatcher.dispatch(self.op_name, backend_type),
                                fn_kwargs = x_args, tensor_gen_kwargs={'map_device': get_torch_map_device(backend_type)})
                if 'after_backend' in self.callback_fn_dict:
                    for callback in self.callback_fn_dict['after_backend']:
                        callback(self.x_names[0], x_args[self.x_names[0]], 'speed', ret)
        if 'after_run' in self.callback_fn_dict:
            for callback in self.callback_fn_dict['after_run']:
                callback(self.x_names[0], x_args[self.x_names[0]], 'speed')