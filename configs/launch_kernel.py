'''
Author       : Thinksky5124
Date         : 2024-03-26 20:41:11
LastEditors  : Thinksky5124
LastEditTime : 2024-04-22 21:24:04
Description  : file content
FilePath     : /AIHPC-Larning/configs/launch_kernel.py
'''
import torch

LOGGER_LIST = dict(
    PythonLoggingLogger = dict(
        name = "AIHPC"
    ),
    # CCLoggerWrapper = dict(
    #     name = "AIHPC"
    # )
)

PROCESSOR = dict(
    type = "SingleProcessor",
    benchmarks = [
        dict(type = "OpKernelBenchmark",
             op_name = "add",
             backends = ["triton", "torch_cpu", "cuda", "openmp"],
            #  data_provider = dict(
            #      type = "DictDataProvider",
            #      gbps = lambda ms, size: 12 * size / ms * 1e-6,
            #      args_dict = dict(
            #          x = dict(type = "RandomTensorGenerator",
            #                   dtype = torch.float32,
            #                   device = "cuda"),
            #          y = dict(type = "RandomTensorGenerator",
            #                   dtype = torch.float32,
            #                   device = "cuda")         
            #      )
            #  ),
            data_provider = dict(
                 type = "TupleDataProvider",
                 gbps = lambda ms, size: 12 * size / ms * 1e-6,
                 args_list = [
                    dict(type = "RandomTensorGenerator",
                              dtype = torch.float32),
                    dict(type = "RandomTensorGenerator",
                              dtype = torch.float32) 
                 ]
             ),
             x_names = ['size'],
             x_vals = [2**i for i in range(12, 28, 1)],
             quantiles = [0.5, 0.2, 0.8])
    ],
    reporters = [
        dict(type = "FigureReporter",
             save_path = "output",
             plot_name = "vector-add-performance",
             line_names = ['Triton', 'TorchCPU', 'CUDA', 'OpenMP'],
             x_names = ['size'],
             x_log=True,
             styles=[('blue', '-'), ('green', '-'), ('red', '-'), ('black', '-')],
             ylabel='GB/s',)
    ]
)