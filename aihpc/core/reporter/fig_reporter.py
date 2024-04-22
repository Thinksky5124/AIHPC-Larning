'''
Author       : Thinksky5124
Date         : 2024-04-06 16:23:51
LastEditors  : Thinksky5124
LastEditTime : 2024-04-22 16:42:46
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/reporter/fig_reporter.py
'''
import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Tuple, Any

from .base_reporter import BaseReporter
from ..utils import ObjectRegister, get_logger

@ObjectRegister.register('reporter')
class FigureReporter(BaseReporter):
    def __init__(self,
                 save_path: str,
                 plot_name: str,
                 x_names: List[str],
                 line_names: List[str],
                 logger_name: str = 'AIHPC',
                 xlabel: str = '',
                 ylabel: str = '',
                 x_log: bool = False,
                 y_log: bool = False,
                 styles = None,
                 show_plots: bool = False,
                 print_data: bool = True) -> None:
        super().__init__(save_path)
        self.plot_name = plot_name
        self.line_names = line_names
        self.logger_name = logger_name
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.x_names = x_names
        self.x_log = x_log
        self.y_log = y_log
        self.styles = styles
        self.show_plots = show_plots
        self.print_data = print_data
        y_min = [f'{x}-min' for x in self.line_names]
        y_max = [f'{x}-max' for x in self.line_names]
        self.df = pd.DataFrame(columns=[self.x_names[0]] + self.line_names + y_min + y_max)
        self.x_names = []
        self.performance_dict = {}

    def __call__(self, x_name: str, x_val: Any, y_name: str, ret: Tuple[Any]) -> None:
        if x_name not in self.x_names:
            self.x_names.append(x_name)
            self.performance_dict[x_name] = dict()
        if x_val not in self.performance_dict[x_name]:
            self.performance_dict[x_name][x_val] = dict()
            self.performance_dict[x_name][x_val]['row_mean'] = []
            self.performance_dict[x_name][x_val]['row_min'] = []
            self.performance_dict[x_name][x_val]['row_max'] = []

        try:
            y_mean, y_min, y_max = ret
        except TypeError:
            y_mean, y_min, y_max = ret, None, None

        self.performance_dict[x_name][x_val]['row_mean'] += [y_mean]
        self.performance_dict[x_name][x_val]['row_min'] += [y_min]
        self.performance_dict[x_name][x_val]['row_max'] += [y_max]

    def save(self, save_path: str = None) -> None:
        if save_path is None:
            save_path = self.save_path
            
        for x_name, y_dict in self.performance_dict.items():
            for x_val, val in y_dict.items():
                self.df.loc[len(self.df)] = [x_val] + val['row_mean'] + val['row_min'] + val['row_max']
            
        if self.plot_name:
            plt.figure()
            ax = plt.subplot()
            x = self.x_names[0]
            for i, y in enumerate(self.line_names):
                y_min, y_max = self.df[y + '-min'], self.df[y + '-max']
                col = self.styles[i][0] if self.styles else None
                sty = self.styles[i][1] if self.styles else None
                ax.plot(self.df[x], self.df[y], label=y, color=col, ls=sty)
                if y_min is not None and y_max is not None:
                    ax.fill_between(self.df[x], y_min, y_max, alpha=0.15, color=col)
            ax.legend()
            xlabel = self.xlabel if self.xlabel else " = ".join(self.x_names)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(self.ylabel)
            ax.set_title(self.plot_name)
            ax.set_xscale("log" if self.x_log else "linear")
            ax.set_yscale("log" if self.y_log else "linear")
            if self.show_plots:
                plt.show()
            if save_path:
                plt.savefig(os.path.join(save_path, f"{self.plot_name}.png"))
        self.df = self.df[[self.x_names[0]] + self.line_names]
        if self.print_data:
            get_logger(self.logger_name).info(f'{self.plot_name}:')
            get_logger(self.logger_name).info("\n" + self.df.to_string())
        if save_path:
            self.df.to_csv(os.path.join(save_path, f"{self.plot_name}.csv"), float_format='%.1f', index=False)
    
    def clear(self) -> None:
        y_min = [f'{x}-min' for x in self.line_names]
        y_max = [f'{x}-max' for x in self.line_names]
        self.df = pd.DataFrame(columns=[self.x_names[0]] + self.line_names + y_min + y_max)
        self.x_names = []
        self.performance_dict = {}