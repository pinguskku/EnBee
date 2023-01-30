import os
import modules.util as util
import constants.constants as Constants

# set current absolute path
absolute_path = os.getcwd()

def not_estimated_commits():
    latest_commits = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "latest_package_manage_system_buggy/go-ethereum_latest_package_manage_system_commits.csv")
    after_commits = os.listdir(absolute_path + Constants.REPORT_RESULT_PATH + "after_buggy/")
    after_commits = [after_commit.split(".")[0] for after_commit in after_commits]

    current_commits = latest_commits["current_commit_id"]
    parent_commits = latest_commits["parent_commit_id"]

    # print(after_commits)
    # print(current_commits)
    # print(parent_commits)

    total_commits = []
    total_commits.extend(current_commits)
    total_commits.extend(parent_commits)

    # print(after_commits)

    not_in_commits = []

    for total_commit in total_commits:
        if total_commit not in after_commits:
            not_in_commits.append(total_commit)

    print(not_in_commits)
    print(len(not_in_commits))



def extract_energy_bug_commits():
    latest_commits = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "latest_package_manage_system_buggy/go-ethereum_latest_package_manage_system_commits.csv")

    current_commits = latest_commits["current_commit_id"]
    parent_commits = latest_commits["parent_commit_id"]

    # save current commit's energy
    for current_commit in current_commits:
        no_value = False

        total_energy = 0
        try:
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "after_buggy/" + current_commit + ".csv", mode='r')
            contents = f.readlines()
            contents = contents[1:]
            f.close()
        except FileNotFoundError:
            no_value = True
    
        if no_value == False:
            for content in contents:
                try:
                    energy_candidate = content.split(",")[12]
                    energy = float(format(float(energy_candidate), 'f'))
                    
                    total_energy = total_energy + energy  # convert to joule

                    finally_total_energy = format(float(total_energy), 'f')

                except ValueError:
                    pass
            
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/go-ethereum_" + str(current_commit) + ".energy", 'w')
            f.write(str(finally_total_energy))
            f.close()

    # save parent commit's energy
    for parent_commit in parent_commits:
        no_value = False

        total_energy = 0
        try:
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "after_buggy/" + parent_commit + ".csv", mode='r')
            contents = f.readlines()
            contents = contents[1:]
            f.close()
        except FileNotFoundError:
            no_value = True
    
        if no_value == False:
            for content in contents:
                try:
                    energy_candidate = content.split(",")[12]
                    energy = float(format(float(energy_candidate), 'f'))
                    
                    total_energy = (total_energy + energy)  # convert to joule

                    finally_total_energy = format(float(total_energy), 'f')

                except ValueError:
                    pass
            
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/go-ethereum_" + str(parent_commit) + ".energy", 'w')
            f.write(str(finally_total_energy))
            f.close()

    # same (current, parent)
    size = len(current_commits)

    # real energy bugg commits
    real_energy_buggy_commits = dict()

    for i in range(size):
        no_value = False

        current_commit_id = current_commits[i]
        parent_commit_id = parent_commits[i]

        try:
            current_content = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/go-ethereum_" + str(current_commit_id) + ".energy", 'r', encoding="CP949")
            parent_content = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/go-ethereum_" + str(parent_commit_id) + ".energy", 'r', encoding="CP949")

            current_commit_energy = format(float(current_content.readline()), '.8f')
            parent_commit_energy = format(float(parent_content.readline()), '.8f')
            # print(current_commit_energy)
            # print(parent_commit_energy)

            current_commit_energy = float(current_commit_energy) * 3600000
            parent_commit_energy = float(parent_commit_energy) * 3600000
            print("==============")
        except FileNotFoundError:
            no_value = True
        
        if no_value == False:
            if current_commit_energy < parent_commit_energy:
                energies = [current_commit_energy, parent_commit_energy]

                real_energy_buggy_commits[current_commit_id + "," + parent_commit_id] = energies
    
    print("energy buggy commits")
    print(real_energy_buggy_commits)
    print(len(real_energy_buggy_commits))

    # for parent_commit in parent_commits:
    #     print(parent_commit)

    # print(len(current_commits))
    # print(len(parent_commits))

    # print(current_energies)
    # print(parent_energies)

    # empty_df = util.get_empty_df()
    # empty_df["current_commit_energy"] = current_energies
    # empty_df["parent_commit_energy"] = parent_energies
    # empty_df.to_csv(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/go-ethereum_commit_energy.csv", index = False)

# not_estimated_commits()
extract_energy_bug_commits()