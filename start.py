import modules.energy_check as ec
import modules.util as util
import os
import constants.constants as Constants
import subprocess
import requests
from bs4 import BeautifulSoup
import time
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import sys
import copy
import subprocess
from codecarbon import EmissionsTracker
from codecarbon import track_emissions
import argparse

def change_pwd(path):
    os.chdir(path)

parser = argparse.ArgumentParser(description='description of usage')

parser.add_argument('--datas', required=True, help='path of github link file.csv')


args = parser.parse_args()
project_link_path = args.datas

projects = util.read_from_csv(project_link_path)['link']

# projects = [
#     "ethereum/go-ethereum",
#     "ava-labs/avalanchego",
#     "etclabscore/core-geth",
#     # "hyperledger/besu",
#     "bobanetwork/boba",
#     "maticnetwork/bor",
#     "BitcoinAssetChain/BTA-CHAIN",
#     "Bytom/bytom",
#     "cube-network/Cube",
#     "Dithereum/Dithereum-Core",
#     "double-a-chain-cloud/double-a-chain",
#     "FUSIONFoundation/efsn",
#     "energicryptocurrency/energi",
#     "ledgerwatch/erigon",
#     "Ether1Project/Ether1",
#     "evmos/evmos",
#     "EZChain-core/ezcgo",
#     "gochain/gochain",
#     "ShyftNetwork/go-empyrean",
#     "Evanesco-Labs/go-evanesco",
#     "hpb-project/go-hpb",
#     "good-data-foundation/goodata-chain",
#     "TechPay-io/go-photon",
#     "quadrans/go-quadrans",
#     "QuarkChain/goquarkchain",
#     "ThinkiumGroup/go-thinkium",
#     "ubiq/go-ubiq",
#     "wanchain/go-wanchain",
#     "Dev-JamesR/go-xerom",
#     "HaloNetwork/Halo_Source_Code",
#     "iotexproject/iotex-core",
#     "Kava-Labs/kava",
#     "klaytn/klaytn",
#     "ontio/ontology",
#     "smartbch/smartbch",
#     "gitter-badger/tao2",
#     "teleport-network/teleport",
#     "thetatoken/theta-protocol-ledger",
#     "tomochain/tomochain",
#     "hash-laboratories-au/XDPoSChain",
#     "xt-smartchain/xsc-chain",
#     "Zenith-Chain/Zenithchain",
#     "ZYXnetwork/ZYX-20-v1"        
# ]

# set current absolute path
absolute_path = os.getcwd()

# change pwd: original_projects
change_pwd(absolute_path + Constants.ORIGINAL_PROJECTS)

global_tc_exist_commits_file_paths = None
global_energy_estimated_output_file = ""

failed_commits = []



def calc_energy(commit_id, current_cmd1, current_cmd2, current_cmd3, current_cmd4, current_cmd5, current_cmd6, test_file_paths):
    for test_file_path in test_file_paths:
        only_test_file_paths = test_file_path.split("/")
        only_test_file_paths = only_test_file_paths[:-1]
        only_test_file_path_name = '/'.join(only_test_file_paths)


        change_pwd(current_cmd1)
        trash_result1 = execute_sync_command_with_return(current_cmd2)

        trash_result2 = execute_sync_command_with_return(current_cmd3)
        
        change_pwd(current_cmd4 + only_test_file_path_name)
        trash_result3 = execute_sync_command_with_return(current_cmd5)

        trash_result4 = execute_sync_command_with_return(current_cmd6)


def execute_command_with_no_return(cmd):
    os.system(cmd)


def execute_command_with_return(cmd):
    output = os.popen(cmd).read()
    return output


def execute_sync_command_with_return(cmd):
    # run the command and wait for it to complete
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode()

def execute_sync_command_with_return_for_error_detect(cmd):
    # run the command and wait for it to complete
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    out = proc.communicate()
    return out


def get_buggy_commits_info(project):
    project_name = project.split("/")[1] # extract project real name
    
    # change CWD (project folder)
    change_pwd(absolute_path + "/original_projects/" + project_name)

    # exact match with "bug" keyword in commit title or content
    # ignore merge commit (becasue to avoid duplication)
    # If you have any techniques to collect buggy commits, let's change below code.

    cmd = 'git log --pretty=format:"%H|%s|%b" --no-merges | grep -w "bug"'
    result = execute_command_with_return(cmd)
    return result


def get_buggy_commit_ids_from_commit_info(commit_infos):
    commit_ids = []
    try:
        commit_all = commit_infos.split("\n")
        for commit in commit_all:
            commit_datas = commit.split("|")
            commit_id = commit_datas[0]

            # check real commit_id
            # avoid to trash variable
            if len(commit_id) == 40:
                if ' ' not in commit_id:
                    commit_ids.append(commit_id)
    except:
        return [Constants.ENBIE_COMMIT_PARSE_ERROR]

    return commit_ids


def get_buggy_issues_info(project):
    token = util.select_token()
    
    # get all issues in repositories
    headers = {"Accept" : "application/vnd.github+json",
    "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28"}

    response = requests.get("https://api.github.com/repos/"+ str(project) + "/issues?state=closed&type=bug",headers=headers)
    body = response.json()

    issue_report_infos = []

    for i in range(len(body)):
        try:
            element = body[i]
            issue_report_infos.append(element["pull_request"]["html_url"])
        except:
            pass

    return issue_report_infos


def get_linked_buggy_commits(project, pull_number):
    token = util.select_token()
    commit_ids = []

    # get all linked commits in issue
    headers = {"Accept" : "application/vnd.github+json",
    "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28"}

    response = requests.get("https://api.github.com/repos/"+ str(project) + "/pulls/" + str(pull_number) + "/commits",headers=headers)
    body = response.json()
    
    # extract commi_ids
    for element in body:
        try:
            commit_id = element["sha"]
            commit_ids.append(commit_id)
        except:
            pass
    
    return commit_ids


def get_buggy_commit_ids_from_issue_info(project, issue_infos):
    commit_ids = []

    try:
        for issue_info in issue_infos:
            before_pull_number = issue_info.split("/")
            pull_number = before_pull_number[len(before_pull_number)-1]

            # get linked commit ids from issue number (pull number)
            each_pull_commit_ids = get_linked_buggy_commits(project, pull_number)
            commit_ids.extend(each_pull_commit_ids)
    except:
        return [Constants.ENBIE_COMMIT_PARSE_ERROR]

    return commit_ids


def filter_commits_exist_tc(project):
    token = util.select_token()
    tc_exist_commits = []
    tc_exist_commits_file_paths = dict()

    project_name = project.split("/")[1]

    buggy_commits = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "buggy/" + project_name + "_buggy_commits.csv")["commit_id"]

    # check tc
    for buggy_commit in buggy_commits:
        try:
            # check commit with tc exist
            headers = {"Accept" : "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28"}
            response = requests.get("https://api.github.com/repos/"+ str(project) + "/commits/" + str(buggy_commit),headers=headers)
            body = response.json()

            files = body["files"]

            tc_file_paths = []
            already_insert = False

            # check tc file
            for file in files:
                is_tc_file = util.test_file_verify(file["filename"])

                # real tc
                if is_tc_file == True:
                    # programming langugage
                    if file["filename"].endswith(Constants.GOLANG_EXTENSION):
                        tc_file_paths.append(file["filename"])

                        # remove commit when TC is not present and is added
                        additions = file["additions"]
                        changes = file["changes"]
                        file_status = additions - changes
                        # if(file_status == 0):
                        #     print(buggy_commit)

                        if file_status != 0 and already_insert == False:
                            tc_exist_commits.append(buggy_commit)
                            already_insert = True

            tc_exist_commits_file_paths[buggy_commit] = tc_file_paths

        except:
            pass
    
    # check


    return tc_exist_commits, tc_exist_commits_file_paths


def remove_duplicate_exist_tc(project):
    all_buggy_commits = []
    all_tc_buggy_commits = []

    project_name = project.split("/")[1]

    all_buggy_commits_candidates = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "buggy/" + project_name + "_buggy_commits.csv")
    all_buggy_commits.extend(all_buggy_commits_candidates['commit_id'])

    all_tc_buggy_commits_candidates = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "tc_buggy/" + project_name + "_tc_buggy_commits.csv")
    all_tc_buggy_commits.extend(all_tc_buggy_commits_candidates['tc_commit_id'])


    purified_all_buggy_commits = util.remove_duplicate(all_buggy_commits)
    purified_all_tc_buggy_commits = util.remove_duplicate(all_tc_buggy_commits)

    # print("buggy: ", purified_all_buggy_commits)
    # print("tc_buggy: ", purified_all_tc_buggy_commits)

    # print("buggy: ", len(purified_all_buggy_commits))
    # print("tc_buggy: ", len(purified_all_tc_buggy_commits))

    return purified_all_buggy_commits, purified_all_tc_buggy_commits


def save_all_commits_each_project(purified_all_tc_buggy_commits, project):
    copied_all_tc_buggy_commits = copy.deepcopy(purified_all_tc_buggy_commits)
    
    project_commits = dict()

    try:
        project_name = project.split("/")[1]

        original_tc_buggy_commits = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "tc_buggy/" + project_name + "_tc_buggy_commits.csv")
        original_tc_buggy_commits = original_tc_buggy_commits["tc_commit_id"]

        # for experimental commits
        uniqued_tc_buggy_commits = list(set(original_tc_buggy_commits) & set(copied_all_tc_buggy_commits))
        copied_all_tc_buggy_commits = list(set(copied_all_tc_buggy_commits) - set(original_tc_buggy_commits))

        # save experimental commits to csv
        util.save_to_csv(uniqued_tc_buggy_commits, [project_name + "_commit_id"], absolute_path + Constants.REPORT_RESULT_PATH + "before_buggy/" + project_name + "_before_buggy_commits.csv")

        project_commits[project_name] = uniqued_tc_buggy_commits
    except:
        pass

    # option: display info
    # for project in projects:
    #     try:
    #         project_name = project.split("/")[1]
    #         data_size = len(project_commits[project_name])
    #         print(data_size)
    #     except:
    #         pass

    return project_commits


def match_current_parent_commits(project, project_commits):
    token = util.select_token()

    project_name = project.split("/")[1]
    commits = project_commits[project_name]

    # get all issues in repositories
    headers = {"Accept" : "application/vnd.github+json",
    "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28"}

    parent_matched_commits = []

    for commit in commits:
        try:
            response = requests.get("https://api.github.com/repos/"+ str(project) + "/git/commits/" + str(commit),headers=headers)
            body = response.json()

            parents = body["parents"]

            # only have on parents
            if len(parents) == 1:
                parent_commit_id = parents[0]["sha"]
                saved_commit_ids = commit + "/" + parent_commit_id

                parent_matched_commits.append(saved_commit_ids)
        except:
            pass

    return parent_matched_commits


def save_parent_matched_commits(parent, parent_matched_commits):
    project_name = project.split("/")[1]

    current_commit_ids = []
    parent_commit_ids = []

    for parent_matched_commit in parent_matched_commits:
        matched_commits = parent_matched_commit.split("/")

        current_commit_id = matched_commits[0]
        parent_commit_id = matched_commits[1]

        current_commit_ids.append(current_commit_id)
        parent_commit_ids.append(parent_commit_id)
    
    empty_df = util.get_empty_df()
    empty_df["current_commit_id"] = current_commit_ids
    empty_df["parent_commit_id"] = parent_commit_ids

    empty_df.to_csv(absolute_path + Constants.REPORT_RESULT_PATH + "parent_matched_buggy/" + project_name + "_parent_matched_buggy_commits.csv", index = False)
    


def ignore_old_package_manage_system_commits(project):
    
    latest_package_manage_system_commits = []
    project_name = project.split("/")[1]

    parent_matched_commits = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "parent_matched_buggy/" + project_name + "_parent_matched_buggy_commits.csv")

    current_commit_ids = parent_matched_commits["current_commit_id"]
    parent_commit_ids = parent_matched_commits["parent_commit_id"]

    for i in range(len(current_commit_ids)):
        try:
            current_commit_id = current_commit_ids[i]
            parent_commit_id = parent_commit_ids[i]

            current_commit_status = False
            parent_commit_status = False

            # change pwd: project path
            change_pwd(absolute_path + Constants.ORIGINAL_PROJECTS + project_name)

            ###################################check current start###################################
            # checkout: current commit
            # original execute_command_with_return
            current_fatal_errors = list(execute_sync_command_with_return_for_error_detect(["/usr/bin/git", "checkout", current_commit_id]))

            current_id_fatal = False
            for current_fatal_error in current_fatal_errors:
                result = current_fatal_error.decode('utf-8')
                if "fatal" in result:
                    current_id_fatal = True

            if current_id_fatal == True:
                continue


            # check whether exist "go.mod" and "go.sum" files
            current_body_mod = execute_command_with_return("ls go.mod go.sum")

            if "No" not in current_body_mod:
                current_commit_status = True
            ###################################check current end###################################


            ###################################check parent start###################################
            # checkout: parent commit
            # original execute_command_with_return
            parent_fatal_errors = list(execute_sync_command_with_return_for_error_detect(["/usr/bin/git", "checkout", parent_commit_id]))

            parent_id_fatal = False
            for parent_fatal_error in parent_fatal_errors:
                result = parent_fatal_error.decode('utf-8')
                if "fatal" in result:
                    parent_id_fatal = True
            
            if parent_id_fatal == True:
                continue

            # check whether exist "go.mod" and "go.sum" files
            parent_body_mod = execute_command_with_return("ls go.mod go.sum")

            if "No" not in parent_body_mod:
                parent_commit_status = True
            ###################################check parent end###################################\

            if current_commit_status == True and parent_commit_status == True:
                saved_commit_ids = current_commit_id + "/" + parent_commit_id
                latest_package_manage_system_commits.append(saved_commit_ids)
        except:
            pass

    return latest_package_manage_system_commits


def save_latest_package_manage_system_commits(project, latest_package_manage_system_commits):
    project_name = project.split("/")[1]

    current_commit_ids = []
    parent_commit_ids = []

    for parent_matched_commit in latest_package_manage_system_commits:
        matched_commits = parent_matched_commit.split("/")

        current_commit_id = matched_commits[0]
        parent_commit_id = matched_commits[1]

        current_commit_ids.append(current_commit_id)
        parent_commit_ids.append(parent_commit_id)
    
    empty_df = util.get_empty_df()
    empty_df["current_commit_id"] = current_commit_ids
    empty_df["parent_commit_id"] = parent_commit_ids

    empty_df.to_csv(absolute_path + Constants.REPORT_RESULT_PATH + "latest_package_manage_system_buggy/" + project_name + "_latest_package_manage_system_commits.csv", index = False)


def estimate_energy_diff_current_parent(project, latest_package_manage_system_commits):
    project_name = project.split("/")[1]
    
    util.createFolder(absolute_path + Constants.REPORT_RESULT_PATH + "/after_buggy/" + project_name)
    print(project_name)
    print(latest_package_manage_system_commits)

    for parent_matched_commit in latest_package_manage_system_commits:
        matched_commits = parent_matched_commit.split("/")

        current_commit_id = matched_commits[0]
        parent_commit_id = matched_commits[1]
        
        try:
            test_file_paths = global_tc_exist_commits_file_paths[current_commit_id]
        except:
            continue
        

        ################ Energy Estimate Start with current_commid_id ################

        current_cmd1 = absolute_path + "/original_projects/" + project_name
        current_cmd2 = "git checkout " + current_commit_id
        current_cmd3 = "go mod tidy"
        current_cmd4 = absolute_path + "/original_projects/" + project_name + "/"
        current_cmd5 = "go mod vender"
        current_cmd6 = "go test"

        print("current", current_commit_id)
        print("parent:" , parent_commit_id)
        current_tracker = ec.get_tracker(absolute_path + Constants.REPORT_RESULT_PATH + "/after_buggy/" + project_name + "/" + str(current_commit_id) + ".csv")
        current_tracker.start()
        try:
            calc_energy(current_commit_id, current_cmd1, current_cmd2, current_cmd3, current_cmd4, current_cmd5, current_cmd6, test_file_paths)
            current_tracker.stop()
        except FileNotFoundError:
            current_tracker.stop()
            continue
        ################ Energy Estimate End with current_commid_id ################

        # time.sleep(1)
        print("current_commit success")

        ################ Energy Estimate Start with parent_commit_id ################
        
        parent_cmd1 = absolute_path + "/original_projects/" + project_name
        parent_cmd2 = "git checkout " + parent_commit_id
        parent_cmd3 = "go mod tidy"
        parent_cmd4 = absolute_path + "/original_projects/" + project_name + "/"
        parent_cmd5 = "go mod vender"
        parent_cmd6 = "go test"

        parent_tracker = ec.get_tracker(absolute_path + Constants.REPORT_RESULT_PATH + "/after_buggy/" + project_name + "/" + str(parent_commit_id) + ".csv")
        parent_tracker.start()
        try:
            calc_energy(parent_commit_id, parent_cmd1, parent_cmd2, parent_cmd3, parent_cmd4, parent_cmd5, parent_cmd6, test_file_paths)
            parent_tracker.stop()
        except FileNotFoundError:
            parent_tracker.stop()
            continue

        ################ Energy Estimate End with parent_commit_id ################

        # time.sleep(1)
        print("parent_commit success")


def extract_energy_bug_commits(project_name):
    final_result = dict()

    util.createFolder(absolute_path + Constants.REPORT_RESULT_PATH + "/commit_energy/" + project_name)

    latest_commits = util.read_from_csv(absolute_path + Constants.REPORT_RESULT_PATH + "latest_package_manage_system_buggy/go-ethereum_latest_package_manage_system_commits.csv")

    current_commits = latest_commits["current_commit_id"]
    parent_commits = latest_commits["parent_commit_id"]

    # save current commit's energy
    for current_commit in current_commits:
        no_value = False

        total_energy = 0
        try:
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "after_buggy/" + project_name + "/" + current_commit + ".csv", mode='r')
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
                    
                    total_energy = energy  # convert to joule

                    finally_total_energy = format(float(total_energy), 'f')

                except ValueError:
                    pass
            
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/" + project_name + "/" + str(current_commit) + ".energy", 'w')
            f.write(str(finally_total_energy))
            f.close()

    # save parent commit's energy
    for parent_commit in parent_commits:
        no_value = False

        total_energy = 0
        try:
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "after_buggy/" + project_name + "/" + parent_commit + ".csv", mode='r')
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
                    
                    total_energy = energy  # convert to joule

                    finally_total_energy = format(float(total_energy), 'f')

                except ValueError:
                    pass
            
            f = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/" + project_name + "/" + str(parent_commit) + ".energy", 'w')
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
            current_content = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/" + project_name + "/" + str(current_commit_id) + ".energy", 'r', encoding="CP949")
            parent_content = open(absolute_path + Constants.REPORT_RESULT_PATH + "commit_energy/" + project_name + "/" + str(parent_commit_id) + ".energy", 'r', encoding="CP949")
            current_commit_energy = format(float(current_content.readline()), '.8f')
            parent_commit_energy = format(float(parent_content.readline()), '.8f')


            current_commit_energy = float(current_commit_energy) * 3600000
            parent_commit_energy = float(parent_commit_energy) * 3600000
            # print("==============")
            # print(current_commit_energy)
            # print(parent_commit_energy)
        except FileNotFoundError:
            no_value = True
        
        if no_value == False:
            if current_commit_energy < parent_commit_energy:
                energies = [current_commit_energy, parent_commit_energy]

                real_energy_buggy_commits[current_commit_id + "," + parent_commit_id] = energies
    
    final_result[project_name] = real_energy_buggy_commits

    return final_result


def save_energy_bug_commits(final_result, project_name):
    print(project_name)
    project_data = final_result[project_name]

    temp_datas = []
    if(len(project_data) > 0):
        keys = project_data.keys()

        for key in keys:
            commit_pair = key.split(",")
            energy_pair = project_data[key]
            current_commit = commit_pair[0]
            parent_commit = commit_pair[1]

            current_energy = energy_pair[0]
            parent_energy = energy_pair[1]
            
            temp_data = [current_commit, parent_commit, current_energy, parent_energy]
            temp_datas.append(temp_data)

    util.save_to_csv(temp_datas, ["current_commit_id", "parent_commit_id", "current_energy", "parent_energy"], absolute_path + Constants.REPORT_RESULT_PATH + "energy_bugs/" + project_name + "_energy_bug_commits.csv")



# Follow steps
# 1) original_projects
# 2) report_results/buggy/
# 3) report_results/tc_buggy/
for obj in projects:
    target_project_infos = obj.split("/")
    project = target_project_infos[-2] + "/" + target_project_infos[-1].replace(".git", "")
    print(project)

    project_name = project.split("/")[1]
    print("start: ", project_name)

    # change pwd: original_projects
    change_pwd(absolute_path + Constants.ORIGINAL_PROJECTS)

    # 1. git cloning
    buggy_commits = []

    print("git clone https://github.com/" + str(project) + ".git")
    dummy_result = execute_sync_command_with_return("git clone https://github.com/" + str(project) + ".git")

    # 2. identify buggy commits (exact match with "bug" keyword in commit title or content)
    buggy_commits_info = get_buggy_commits_info(project)
    commit_ids_from_info = get_buggy_commit_ids_from_commit_info(buggy_commits_info)

    if len(commit_ids_from_info) == Constants.ENBIE_COMMIT_PARSE_ERROR:
        print(Constants.ENBIE_COMMIT_PARSE_ERROR)
        sys.exit(1)

    # 3. identify buggy commits (Issue card must to have linked commit. In other words, Pull Request)
    # 3.1 Extract All Issues (state: closed, label: bug)
    buggy_issues_info = get_buggy_issues_info(project)

    # 3.2 Extract All Linked Commits (If exist pull request)
    commit_ids_from_issue = get_buggy_commit_ids_from_issue_info(project, buggy_issues_info)

    # 4. Merge All buggy commits
    buggy_commits.extend(commit_ids_from_info)
    buggy_commits.extend(commit_ids_from_issue)

    buggy_commits = util.remove_duplicate(buggy_commits)
    
    # 5. Save Buggy Commits to CSV
    util.save_to_csv(buggy_commits, ["commit_id"], absolute_path + Constants.REPORT_RESULT_PATH + "buggy/" + project_name + "_buggy_commits.csv")

    # 6. Filters commit with TC
    # Also, remove non programming language file (current support golang .go)
    # Also, remove commit when TC is not present and is added.
    tc_exist_commits, tc_exist_commits_file_paths = filter_commits_exist_tc(project)
    global_tc_exist_commits_file_paths = tc_exist_commits_file_paths

    # 6.1 Save Buggy Commits with TC to CSV
    util.save_to_csv(tc_exist_commits, ["tc_commit_id"], absolute_path + Constants.REPORT_RESULT_PATH + "tc_buggy/" + project_name + "_tc_buggy_commits.csv")
    # print(tc_exist_commits)

    # 7. Remove Dupliated Commits (Between All Projects)
    # read all csv
    purified_all_buggy_commits, purified_all_tc_buggy_commits = remove_duplicate_exist_tc(project)

    # 8. Save all commits to each project
    project_commits = save_all_commits_each_project(purified_all_tc_buggy_commits, project)



    # 9. Detect Energy Bug 
    # For this step, Do estimate energy consumption of buggy commit

    # 9.1 extract current, parent commit
    parent_matched_commits = match_current_parent_commits(project, project_commits)
    save_parent_matched_commits(project, parent_matched_commits)
    

    # 9.2 Ignore old version (not incluse automated package manage system)
    # after golang 1.11~~~ (2018 year)
    latest_package_manage_system_commits = ignore_old_package_manage_system_commits(project)
    save_latest_package_manage_system_commits(project, latest_package_manage_system_commits)

    9.3 Estimate Energy Diff With Current and Parent Commits
    before / after
    estimate_energy_diff_current_parent(project, latest_package_manage_system_commits)

    final_result = extract_energy_bug_commits(project_name)

    save_energy_bug_commits(final_result, project_name)
