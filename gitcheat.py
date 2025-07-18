import os
import subprocess
import shutil
import re
import logging
import random
import time
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(message)s")

def run_command(command, exit_on_error=True):
    """Run a shell command and handle errors."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error: {result.stderr}")
        if exit_on_error:
            exit(1)
    return result.stdout.strip()

def ensure_git_filter_repo():
    """Ensures that git-filter-repo is installed."""
    logging.info("Checking for git-filter-repo...")
    result = run_command("which git-filter-repo", exit_on_error=False)
    
    if not result:
        logging.info("git-filter-repo not found. Installing...")
        try:
            # Try installing with pip to user directory
            run_command("pip install --user git-filter-repo", exit_on_error=False)
            
            # Add ~/.local/bin to PATH temporarily if it exists
            local_bin = os.path.expanduser("~/.local/bin")
            if os.path.exists(local_bin):
                os.environ["PATH"] = f"{local_bin}:{os.environ['PATH']}"
                
            # Verify installation
            if not run_command("which git-filter-repo", exit_on_error=False):
                # Try to download directly and make executable
                logging.info("Downloading git-filter-repo directly...")
                run_command("curl -o git-filter-repo https://raw.githubusercontent.com/newren/git-filter-repo/main/git-filter-repo", exit_on_error=False)
                run_command("chmod +x git-filter-repo", exit_on_error=False)
                run_command("sudo mv git-filter-repo /usr/local/bin/", exit_on_error=False)
                
                if not run_command("which git-filter-repo", exit_on_error=False):
                    logging.error("Failed to install git-filter-repo. Make sure it's properly installed.")
                    logging.error("You can manually install with: pip install --user git-filter-repo")
                    exit(1)
        except Exception as e:
            logging.error(f"Error installing git-filter-repo: {e}")
            exit(1)

def validate_repo_url(url):
    """Validate the repository URL format."""
    if not (url.startswith("http://") or url.startswith("https://") or url.startswith("git@")):
        logging.error(f"Invalid repository URL: {url}")
        exit(1)

def extract_repo_name(url):
    """Extract the repository name from a Git URL."""
    # First try the standard pattern
    match = re.search(r"/([^/]+?)(\.git)?$", url)
    if match:
        return match.group(1).replace(".git", "")
    
    # Try other GitHub URL patterns
    github_match = re.search(r"github\.com/[^/]+/([^/\.]+)", url)
    if github_match:
        return github_match.group(1)
        
    logging.error(f"Could not extract repository name from URL: {url}")
    return None

def generate_random_date_range(start_date, end_date, num_commits):
    """Generate a list of random dates within the specified range."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    if start >= end:
        logging.error("Start date must be before end date")
        return []
    
    # Generate random dates
    dates = []
    time_diff = end - start
    for _ in range(num_commits):
        random_days = random.randint(0, time_diff.days)
        random_seconds = random.randint(0, 86400)  # Random time within the day
        random_date = start + timedelta(days=random_days, seconds=random_seconds)
        dates.append(random_date)
    
    # Sort dates to maintain chronological order
    dates.sort()
    return dates

def get_commit_count(repo_path):
    """Get the total number of commits in the repository."""
    try:
        result = run_command("git rev-list --count --all", exit_on_error=False)
        return int(result) if result else 0
    except:
        return 0

def transfer_repo(old_repo_url, new_repo_url, new_author_name, new_author_email, 
                 replace_in_messages=False, replacements=None, modify_dates=False, 
                 start_date=None, end_date=None):
    """Transfers all branches from the old repo to the new repo with updated authorship and optionally modified dates."""
    bare_repo = None
    
    try:
        validate_repo_url(old_repo_url)
        validate_repo_url(new_repo_url)

        repo_name = extract_repo_name(old_repo_url)
        if not repo_name:
            logging.error("Failed to extract repository name. Exiting.")
            return
            
        bare_repo = f"{repo_name}.git"

        logging.info("Cloning the repository...")
        run_command(f"git clone --bare {old_repo_url}")

        os.chdir(bare_repo)

        ensure_git_filter_repo()

        # Get commit count for date generation
        commit_count = get_commit_count(".")
        
        # Step 1: Update author info and messages
        logging.info("Updating author information...")
        callback_parts = []
        callback_parts.append(f"commit.author_name = commit.committer_name = b'{new_author_name}'")
        callback_parts.append(f"commit.author_email = commit.committer_email = b'{new_author_email}'")
        
        if replace_in_messages and replacements:
            callback_parts.append("message = commit.message.decode('utf-8', errors='replace')")
            for old_text, new_text in replacements.items():
                old_text_escaped = old_text.replace("'", "\\'")
                new_text_escaped = new_text.replace("'", "\\'")
                callback_parts.append(f"message = message.replace('{old_text_escaped}', '{new_text_escaped}')")
            callback_parts.append("commit.message = message.encode('utf-8')")
        
        callback = '; '.join(callback_parts)
        run_command(f'git-filter-repo --commit-callback "{callback}" --force')
        
        # Step 2: Modify dates if requested
        if modify_dates and start_date and end_date:
            logging.info(f"Modifying commit dates to random dates between {start_date} and {end_date}...")
            
            # Generate random dates
            random_dates = generate_random_date_range(start_date, end_date, commit_count)
            
            # Get list of all commits
            commits = run_command("git log --all --format='%H' --reverse").split('\n')
            commits = [c for c in commits if c.strip()]
            
            # Create environment filter script
            env_filter = 'case $GIT_COMMIT in\n'
            
            for i, commit in enumerate(commits):
                if i < len(random_dates):
                    timestamp = int(random_dates[i].timestamp())
                    env_filter += f'    {commit}) export GIT_AUTHOR_DATE="{timestamp}"; export GIT_COMMITTER_DATE="{timestamp}";;\n'
            
            env_filter += '    *) ;;\nesac'
            
            run_command(f'git filter-branch --env-filter \'{env_filter}\' --force -- --all')
            
            run_command('git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d', exit_on_error=False)

        logging.info("Adding new repository remote...")
        run_command(f"git remote add new-origin {new_repo_url}")

        logging.info("Pushing all branches and tags to the new repository...")
        run_command("git push --mirror new-origin")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)

    finally:
        # Only try to change directory and remove the repo if bare_repo exists
        if bare_repo and os.path.exists(bare_repo):
            os.chdir("..")
            shutil.rmtree(bare_repo, ignore_errors=True)
        logging.info("✅ Repository transfer complete!")

if __name__ == "__main__":
    print(r"""
       ____   ___   _____            ____   _   _   _____      _      _____ 
      / ___| |_ _| |_   _|          / ___| | | | | | ____|    / \    |_   _|
     | |  _   | |    | |    _____  | |     | |_| | |  _|     / _ \     | |  
     | |_| |  | |    | |   |_____| | |___  |  _  | | |___   / ___ \    | |  
      \____| |___|   |_|            \____| |_| |_| |_____| /_/   \_\   |_|  
    """ )
    
    old_repo_url = input("Enter the URL of the old repository: ").strip()
    new_repo_url = input("Enter the URL of the new repository: ").strip()
    new_author_name = input("Enter the new author's name: ").strip()
    new_author_email = input("Enter the new author's email: ").strip()
    
    # Ask about date modification
    modify_dates = input("Do you want to modify commit dates? (yes/no): ").strip().lower() in ["yes", "y"]
    start_date = None
    end_date = None
    
    if modify_dates:
        print("\nEnter the date range for randomizing commit dates:")
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        
        # Validate date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            logging.error("Invalid date format. Please use YYYY-MM-DD format.")
            exit(1)
    
    replacements = {}
    while True:
        replace_message = input("Do you want to replace text in commit messages? (yes/no): ").strip().lower()
        if replace_message in ["yes", "y"]:
            old_text = input("Enter the text to replace in commit messages: ").strip()
            new_text = input("Enter the replacement text: ").strip()
            replacements[old_text] = new_text
            print(f"Added replacement: '{old_text}' → '{new_text}'")
        else:
            break
    
    print("\n" + "="*50)
    print("TRANSFER SUMMARY:")
    print(f"Old repository: {old_repo_url}")
    print(f"New repository: {new_repo_url}")
    print(f"New author: {new_author_name} <{new_author_email}>")
    if modify_dates:
        print(f"Date range: {start_date} to {end_date}")
    if replacements:
        print(f"Message replacements: {len(replacements)} replacement(s)")
    print("="*50)
    
    confirm = input("Proceed with transfer? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("Transfer cancelled.")
        exit(0)
    
    # Execute transfer
    transfer_repo(old_repo_url, new_repo_url, new_author_name, new_author_email, 
                 bool(replacements), replacements, modify_dates, start_date, end_date)