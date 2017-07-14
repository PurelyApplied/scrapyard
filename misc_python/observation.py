import pandas as pd
import numpy as np
from tabulate import tabulate


def get_data_per_inst(df, label, n_PIDs, normalization=1):
    retval = sum(
        df[label][df.PID == i].values / normalization
        for i in range(n_PIDs))
    # print(type(retval))
    return retval


class Observation:
    def __init__(self, filename):
        self.filename = filename
        self.CSV = pd.read_csv(filename).rename(columns=lambda x: x.strip())
        self.num_compartments = max(self.CSV.PID) + 1
        self.N = get_data_per_inst(self.CSV, "n_local_nodes", self.num_compartments)[0]
        self.data = {}

        self.make_observations()

    def __repr__(self):
        return "<Observation from file: {}>".format(self.filename)

    def get(self, tag, normalized=True):
        return self._get_data_per_inst(self.CSV, tag,
                                       self.num_compartments,
                                       self.N if normalized else 1)

    def _get_data_per_inst(self, df, label, n_PIDs, normalization=1):
        retval = sum(
            df[label][df.PID == i].values / normalization
            for i in range(n_PIDs))
        # print(type(retval))
        return retval

    def display_tables(self):
        assert self.data, "Data not gathered yet."
        print(tabulate(self.data, headers="keys"))
        self.display_table_summary()

    def display_table_summary(self, **kwargs):
        data = {k: v.mean() for k, v in self.data.items()}
        disp_data = [[k, v] for k, v in sorted(data.items())]
        head = ["Name", "Averge"]
        print(tabulate(disp_data, headers=head, **kwargs))

    def make_observations(self, verbose=False):
        CSV = self.CSV
        n_c = self.num_compartments
        N = self.N
        get_it = self.get

        #####
        # Direct from data
        infected = get_it("cntr_infected")
        total_updates = get_it("cntr_tugs_resolved")
        cascades = get_it("cntr_tug_cascades_resolved")
        ### This has been validated as equal to the above
        # off_thread_cascades = get_it("cntr_tug_cascades_from_off_thread_source")
        messages_sent = get_it("cntr_inf_messages_sent")
        messages_skip = get_it("cntr_inf_messages_pruned_from_sending")
        # This is T or U
        messages_not_ignored = get_it("cntr_inf_messages_not_ignored")
        inf_redundant = get_it("cntr_inf_messages_redundant")
        upd_redundant = get_it("cntr_updating_messages_redundant")
        transmissions = get_it('cntr_transmission_messages_effective')

        #####
        # Computed from data
        computed_first_order_updates = total_updates - cascades
        messages_theoretically_sent = messages_sent + messages_skip
        transmissions_computed = messages_not_ignored - computed_first_order_updates - inf_redundant
        overhead_with_redundancies = messages_theoretically_sent - messages_not_ignored + inf_redundant + upd_redundant
        overhead_without_redundancies = messages_theoretically_sent - messages_not_ignored
        effective_transmissions = transmissions + inf_redundant

        self.data.update({
            "infected": infected,
            "effective_transmission": effective_transmissions,
            "total_updates": total_updates,
            "cascades": cascades,
            # "off_thread_cascades": off_thread_cascades,
            "messages_sent": messages_sent,
            "messages_skip": messages_skip,
            "messages_not_ignored": messages_not_ignored,
            "inf_redundant": inf_redundant,
            "upd_redundant": upd_redundant,
            "computed_first_order_updates": computed_first_order_updates,
            "messages_theoretically_sent": messages_theoretically_sent,
            "transmissions": transmissions,
            "transmissions_computed": transmissions_computed,
            "overhead_with_redundancies": overhead_with_redundancies,
            "overhead_without_redundancies": overhead_without_redundancies,
        })

        if verbose:
            print("Object .data updated.")
            print("Observed means, less redundancies...")
            print("R:", np.mean(infected))
            print("T:", np.mean(transmissions))
            print("U:", np.mean(computed_first_order_updates))
            print("O:", np.mean(overhead_without_redundancies))
            print('Observed total:', np.mean(messages_theoretically_sent))
            print("# actual sent:", np.mean(
                get_data_per_inst(CSV, "cntr_inf_messages_sent", n_c, N)))

    def report_statistics(self):
        '''Report min|.25|median|.75|max|median for each column'''
        assert self.data, "Data not gathered yet."
        report = {}
        for k, v in self.data.items():
            report[k] = [("{}".format(p), np.percentile(v, p))
                         for p in range(0, 101, 25)]
            report[k].append(("AVG:", v.mean()))
        return report
