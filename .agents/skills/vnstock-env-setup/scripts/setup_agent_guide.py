import os
import sys
import shutil
import subprocess
import tempfile
import platform

def run_cmd(cmd, check=True):
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error executing {' '.join(cmd)}:")
        print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()

def check_and_install_git():
    try:
        run_cmd(["git", "--version"])
        print("✅ Git is installed.")
    except Exception:
        print("❌ Git is not installed. Attempting to install...")
        sys_os = platform.system()
        if sys_os == "Darwin":
            run_cmd(["brew", "install", "git"])
        elif sys_os == "Linux":
            run_cmd(["sudo", "apt-get", "update"])
            run_cmd(["sudo", "apt-get", "install", "-y", "git"])
        elif sys_os == "Windows":
            print("Downloading Git for Windows...")
            run_cmd(["powershell", "-Command", "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe -OutFile git_installer.exe"])
            print("Installing Git...")
            run_cmd(["powershell", "-Command", "Start-Process -FilePath .\\git_installer.exe -ArgumentList '/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS' -Wait"])
            if os.path.exists("git_installer.exe"):
                os.remove("git_installer.exe")
        print("✅ Git installation attempted.")

def ensure_git_backup():
    if not os.path.exists(".git"):
        print("📦 No Git repository found. Initializing new repository...")
        run_cmd(["git", "init"])
        run_cmd(["git", "add", "."])
        # Need to handle edge case where identity is not configured
        subprocess.run(["git", "config", "user.email", "agent@vnstocks.com"], capture_output=True)
        subprocess.run(["git", "config", "user.name", "AI Agent"], capture_output=True)
        res = subprocess.run(["git", "commit", "-m", "Initial commit before Agent Guide installation"], capture_output=True)
        if res.returncode == 0:
            print("✅ Initial commit created.")
    else:
        print("📦 Git repository detected. Creating backup commit...")
        run_cmd(["git", "add", "."])
        subprocess.run(["git", "config", "user.email", "agent@vnstocks.com"], capture_output=True)
        subprocess.run(["git", "config", "user.name", "AI Agent"], capture_output=True)
        res = subprocess.run(["git", "commit", "-m", "Backup workspace before Agent Guide installation"], capture_output=True)
        if res.returncode == 0:
            print("✅ Workspace backed up in a commit.")
        else:
            print("ℹ️ Working tree clean. Nothing to commit.")

def install_agent_guide():
    repo_url = "https://github.com/vnstock-hq/vnstock-agent-guide.git"
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📥 Cloning repository to {temp_dir}...")
        run_cmd(["git", "clone", repo_url, temp_dir])
        
        cwd = os.getcwd()
        
        # 1. Copy root files
        for file in ["AGENTS.md", "CLAUDE.md"]:
            src = os.path.join(temp_dir, file)
            # Only copy if file exists in the repo
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(cwd, file))
                print(f"✅ Copied {file}")
                
        # 2. Copy Vnstock skills without overwriting unrelated user custom skills.
        dest_skills_dir = os.path.join(cwd, ".agents", "skills")
        os.makedirs(dest_skills_dir, exist_ok=True)

        src_skills_dir = os.path.join(temp_dir, ".agents", "skills")
        skills_to_copy = sorted(os.listdir(src_skills_dir)) if os.path.exists(src_skills_dir) else []

        for skill in skills_to_copy:
            src_skill = os.path.join(src_skills_dir, skill)
            dest_skill = os.path.join(dest_skills_dir, skill)
            if os.path.isdir(src_skill):
                if os.path.exists(dest_skill):
                    shutil.rmtree(dest_skill)
                shutil.copytree(src_skill, dest_skill)
                print(f"✅ Copied skill: {skill}")
                
        # 3. Copy docs directory (Overwrite)
        src_docs = os.path.join(temp_dir, "docs")
        dest_docs = os.path.join(cwd, "docs")
        if os.path.exists(src_docs):
            if os.path.exists(dest_docs):
                shutil.rmtree(dest_docs)
            shutil.copytree(src_docs, dest_docs)
            print("✅ Copied/Overwrote 'docs' directory")

        # 4. Copy GitHub helper files if present.
        src_github = os.path.join(temp_dir, ".github")
        dest_github = os.path.join(cwd, ".github")
        if os.path.exists(src_github):
            if os.path.exists(dest_github):
                shutil.rmtree(dest_github)
            shutil.copytree(src_github, dest_github)
            print("✅ Copied/Overwrote '.github' directory")

        print("🎉 Agent Guide Installation Complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm-docs-overwrite", action="store_true", help="Confirm overwriting the docs folder")
    args = parser.parse_args()
    
    # We enforce confirmation outside the script via the AI's interaction
    if os.path.exists("docs") and not args.confirm_docs_overwrite:
        print("❌ ERROR: 'docs' directory exists. You must provide --confirm-docs-overwrite to proceed.")
        sys.exit(1)
        
    check_and_install_git()
    ensure_git_backup()
    install_agent_guide()
