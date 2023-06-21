import os
import pandas as pd
import numpy as np
import yaml


class PDS:
    def __init__(self, data_folder):
        self.data_folder = data_folder

        self.bus = pd.read_csv(os.path.join(self.data_folder, 'bus.csv'), index_col=0)
        self.lines = pd.read_csv(os.path.join(self.data_folder, 'lines.csv'), index_col=0)
        self.psh = pd.read_csv(os.path.join(self.data_folder, 'psh.csv'), index_col=0)
        self.dem_active = pd.read_csv(os.path.join(self.data_folder, 'dem_active_power.csv'), index_col=0)
        self.dem_reactive_power = pd.read_csv(os.path.join(self.data_folder, 'dem_reactive_power.csv'), index_col=0)
        self.grid_tariff = pd.read_csv(os.path.join(self.data_folder, 'grid_tariff.csv'), index_col=0)

        self.n_bus = len(self.bus)
        self.n_lines = len(self.lines)
        self.n_psh = len(self.psh)

        self.generators = self.bus.loc[self.bus['type'] == 'reference']
        self.A = self.get_connectivity_mat()

        # read other parameters
        with open(os.path.join(self.data_folder, 'params.yaml'), 'r') as f:
            params = yaml.safe_load(f)
            self.__dict__.update(params)

    def get_bus_lines(self, bus_id):
        return self.lines.loc[(self.lines['from_bus'] == bus_id) | (self.lines['to_bus'] == bus_id)]

    def get_reactance_mat(self):
        y = np.zeros((self.n_bus, self.n_bus))
        pass

    def get_connectivity_mat(self, param=''):
        mat = np.zeros((self.n_bus, self.n_bus))

        start_indices = np.searchsorted(self.bus.index, self.lines.loc[:, 'from_bus'])
        end_indices = np.searchsorted(self.bus.index, self.lines.loc[:, 'to_bus'])
        if param:
            mat_values = self.lines[param]
        else:
            mat_values = 1

        mat[start_indices, end_indices] = mat_values
        return mat