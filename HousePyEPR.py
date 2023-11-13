import pyEPR as epr
import numpy as np
import os
from tqdm import tqdm
#In case of unknown missing packages, install windowscom and pint
#I recommend careful meshing and second order basis function on HFSS
#all the reshaped csv files have resonating mode in columns and variations in row and they're reshaped into this reader friendly mode
class House_PyEPR:
    def __init__(self,**kwargs):
        self.path=kwargs['HFSSproject_path']
        self.name = kwargs['HFSSproject_name']
        self.designname = kwargs['HFSSdesign_name']
        self.index = kwargs['iter_num']
        self.parent_directory=kwargs['savingdirectory']
        self.directory= kwargs['savingfilename']
        self.filepath=os.path.join(self.parent_directory, str(self.directory)+str(self.index))


    def save(self):
        excelfilepath_reshaped = os.path.join(self.filepath, r"reshaped")
        excelfilepath_raw = os.path.join(self.filepath, r"raw")
        os.makedirs(excelfilepath_raw)
        os.makedirs(excelfilepath_reshaped)

    def run(self):

        excelfilepath_reshaped = os.path.join(self.filepath, r"reshaped")
        excelfilepath_raw = os.path.join(self.filepath, r"raw")

        pinfo = epr.ProjectInfo(project_path=self.path,
                                project_name=self.name, design_name=self.designname)
        pinfo.junctions['qubit1'] = {'Lj_variable': 'Q1Lj', 'rect': 'Q1Sheet', 'line': 'Q1Line'}
        pinfo.junctions['qubit2'] = {'Lj_variable': 'Q2Lj', 'rect': 'Q2Sheet', 'line': 'Q2Line'}
        pinfo.junctions['qubit3'] = {'Lj_variable': 'Q3Lj', 'rect': 'Q3Sheet', 'line': 'Q3Line'}

        pinfo.validate_junction_info()
        eprd = epr.DistributedAnalysis(pinfo)
        eprd.do_EPR_analysis(append_analysis=False)
        epra = epr.QuantumAnalysis(eprd.data_filename)

        for i in range(0, len(eprd.variations)):
            epra.analyze_variation(variation=str(eprd.variations[i]), print_result=False)

        epra._hfss_variables
        epra._hfss_variables.to_csv(excelfilepath_reshaped + r"\variation" + self.index + r".csv", sep=",")

        dressed_freq = epra.get_frequencies(numeric=False)
        chi = epra.get_chis(numeric=False)
        Q = epra.get_quality_factors()
        hfss_vars = epra._hfss_variables

        # extract ker in MHz
        # extract all the ker terms
        # self ker without resonator:
        chi_numpy = chi.to_numpy()
        num_rows_chi, num_cols_chi = chi_numpy.shape
        num_variations = eprd.n_variations
        ker_list = []

        for v in tqdm(range(num_variations)):
            for n in tqdm(range(num_cols_chi)):
                ker_list.append(chi_numpy[v * num_cols_chi + n, n])

        ker_numpy = np.array(ker_list)

        np.savetxt(excelfilepath_raw + r"\chi_np" + self.index + r".csv", chi_numpy, delimiter=",")
        np.savetxt(excelfilepath_raw + r"\ker_np" + self.index + r".csv", ker_numpy, delimiter=",")

        self_ker_list = []
        cross_ker_list = []
        for v in tqdm(range(num_variations)):
            for n in tqdm(range(num_cols_chi)):
                m = n + 1
                if m % 4 != 0:
                    self_ker_list.append(ker_list[num_cols_chi * v + n])
                    cross_ker_list.append(chi_numpy[num_cols_chi * v + n, -1])
                else:
                    continue

        self_ker_np = np.array(self_ker_list)
        cross_ker_np = np.array(cross_ker_list)

        np.savetxt(excelfilepath_raw + r"\self_ker" + self.index + r".csv", self_ker_np, delimiter=",")
        np.savetxt(excelfilepath_raw + r"\cross_ker" + self.index + r".csv", cross_ker_np, delimiter=",")

        # abstract qubits Quality factor
        # in Q table, first variation is the analysis result, starting the second col we have the first variatoin result
        # the fourth row (resonator mode that we dont care is skipped)
        # column is variations, row is modes
        Q_qubits_np = Q.to_numpy()[0:num_cols_chi - 1, :]
        np.savetxt(excelfilepath_raw + r"\Q_qubits" + self.index + r".csv", Q_qubits_np, delimiter=",")
        num_rows_Q, num_cols_Q = Q_qubits_np.shape

        # extractqubits frequency in MHz
        dressed_freq_qubits_np = dressed_freq.to_numpy()[0:num_cols_chi - 1, :]
        np.savetxt(excelfilepath_reshaped + r"\dressed_freq_qubits_reshaped" + self.index + r".csv", dressed_freq_qubits_np, delimiter=",")

        # extract kappa of only resonator in MHz
        # frequency and q from hfss has mode as row and variation as coloumn
        kappa_resonator_np = np.divide(dressed_freq.to_numpy()[-1, :], Q.to_numpy()[-1, :])
        # chi_over_kappa needs to be larger or at least equal to 1
        chi_over_kappa = np.empty((num_rows_Q, num_cols_Q))

        # reshape kappa to perform np divide
        # reshape cross ker and self ker
        cross_ker_np_reshaped = cross_ker_np
        self_ker_np_reshaped = self_ker_np.reshape(num_rows_Q, num_cols_Q)
        cross_ker_np_reshaped = cross_ker_np.reshape(num_rows_Q, num_cols_Q)
        n = 1
        kappa_resonator_np_reshaped = kappa_resonator_np
        while n < num_rows_Q:
            kappa_resonator_np_reshaped = np.vstack((kappa_resonator_np_reshaped, kappa_resonator_np))
            n = n + 1
        chi_over_kappa_np = np.divide(cross_ker_np_reshaped, kappa_resonator_np_reshaped)
        np.savetxt(excelfilepath_reshaped + r"\kappa_resonator_reshaped" + self.index + r".csv", kappa_resonator_np_reshaped, delimiter=",")
        np.savetxt(excelfilepath_reshaped + r"\chi_over_kappa_reshaped" + self.index + r".csv", chi_over_kappa_np, delimiter=",")
        np.savetxt(excelfilepath_reshaped + r"\self_ker_reshaped" + self.index + r".csv", self_ker_np_reshaped, delimiter=",")
        np.savetxt(excelfilepath_reshaped + r"\cross_ker_reshaped" + self.index + r".csv", cross_ker_np_reshaped, delimiter=",")


