import subprocess

def extract_best_conformation_in_vina_result(output_file):
    with open(output_file, 'r') as f:
        lines = f.readlines()
    best_score = float('inf')
    best_model = []
    current_model = []
    recording = False
    for line in lines:
        if line.startswith("MODEL"):
            recording = True
            current_model = []
        elif "ENDMDL" in line:
            recording = False
            score_line = [l for l in current_model if "REMARK VINA RESULT" in l]
            if score_line:
                score = float(score_line[0].split()[3])
                if score < best_score:
                    best_score = score
                    best_model = current_model
        if recording:
            current_model.append(line)
    return best_model, best_score

def run_vina_and_extract_best(num_run_vina, vina_path, config_path, task_name, dock_dir):
    best_scores = []
    for i in range(num_run_vina):
        log_file = f"{dock_dir}/log/{task_name}_out_{i+1}.log"
        output_file = f"{dock_dir}/out_pdbqt/{task_name}_out_{i+1}.pdbqt"
        best_output_file = f"{dock_dir}/best_pdbqt/{task_name}_out_{i+1}.pdbqt"
        subprocess.run(f"{vina_path} --config {config_path} --log {log_file} --out {output_file}", shell=True)
        best_model, best_score = extract_best_conformation_in_vina_result(output_file)
        best_scores.append(best_score)
        with open(best_output_file, 'w') as f:
            f.writelines(best_model)
    with open(f"{dock_dir}/best_scores.txt", 'w') as score_file:
        for index, score in enumerate(best_scores, 1):
            score_file.write(f"Run {index}: {score}\n")

