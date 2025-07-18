# Git-Cheat: Repository Transfer Tool

A powerful tool for transferring Git repositories while rewriting commit history, modifying commit messages, and randomizing commit dates.


## Features

- **Complete Repository Transfer**: Transfer all branches and tags from source to destination
- **Author Information Rewriting**: Change author name and email across all commits
- **Commit Message Modification**: Replace text in commit messages (supports multiple replacements)
- **Date Randomization**: Randomly distribute commit dates within a specified date range
- **Automatic Tool Installation**: Automatically installs git-filter-repo if not present
- **Interactive Interface**: User-friendly command-line prompts guide you through the process

## Prerequisites

- Python 3.6+
- Git
- Internet connection (for automatic tool installation)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Pudv95/Git-Cheat.git
   cd Git-Cheat
   ```

2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script using Python:

```bash
python gitcheat.py
```

The script will guide you through the process with interactive prompts:

1. **Repository URLs**: Enter the source and destination repository URLs (HTTPS or SSH)
2. **Author Information**: Provide the new author name and email
3. **Date Modification**: Choose whether to randomize commit dates
   - If yes, specify the date range (YYYY-MM-DD format)
   - Commits will be randomly distributed within this range
4. **Message Replacements**: Optionally replace text in commit messages
   - Add multiple replacements as needed
   - Useful for fixing typos or updating references

## Example Usage

```
$ python gitcheat.py

       ____   ___   _____            ____   _   _   _____      _      _____ 
      / ___| |_ _| |_   _|          / ___| | | | | | ____|    / \    |_   _|
     | |  _   | |    | |    _____  | |     | |_| | |  _|     / _ \     | |  
     | |_| |  | |    | |   |_____| | |___  |  _  | | |___   / ___ \    | |  
      \____| |___|   |_|            \____| |_| |_| |_____| /_/   \_\   |_|  

Enter the URL of the old repository: https://github.com/original-owner/example-repo.git
Enter the URL of the new repository: git@github.com:your-username/example-repo.git
Enter the new author's name: Your Name
Enter the new author's email: your.email@example.com

Do you want to modify commit dates? (yes/no): yes

Enter the date range for randomizing commit dates:
Enter start date (YYYY-MM-DD): 2023-01-01
Enter end date (YYYY-MM-DD): 2023-12-31

Do you want to replace text in commit messages? (yes/no): yes
Enter the text to replace in commit messages: old-company-name
Enter the replacement text: new-company-name
Added replacement: 'old-company-name' → 'new-company-name'

Do you want to replace text in commit messages? (yes/no): no

==================================================
TRANSFER SUMMARY:
Old repository: https://github.com/original-owner/example-repo.git
New repository: git@github.com:your-username/example-repo.git
New author: Your Name <your.email@example.com>
Date range: 2023-01-01 to 2023-12-31
Message replacements: 1 replacement(s)
==================================================

Proceed with transfer? (yes/no): yes

Cloning the repository...
Checking for git-filter-repo...
Updating author information...
Modifying commit dates to random dates between 2023-01-01 and 2023-12-31...
Adding new repository remote...
Pushing all branches and tags to the new repository...
✅ Repository transfer complete!
```

## Use Cases

### Portfolio Cleanup
- Transfer old projects to your personal GitHub
- Update author information to your current details
- Randomize commit dates to show consistent activity
- Remove company-specific references from commit messages

### Repository Migration
- Move repositories between different platforms
- Consolidate multiple repositories under new ownership
- Update historical commits with corrected information

### Privacy Protection
- Anonymize commit history while preserving code changes
- Randomize timing patterns to protect work schedules
- Remove sensitive information from commit messages

## Preparing Your New Repository

Before running the script:

1. **Create an empty repository** on GitHub/GitLab/etc.
2. **Do not initialize** it with README, .gitignore, or license files
3. **Copy the repository URL** (SSH recommended for private repos)
4. **Ensure you have write access** to the destination repository

Example URL formats:
```bash
# SSH URL format (recommended)
git@github.com:username/repository.git

# HTTPS URL format
https://github.com/username/repository.git
```

## How It Works

Git-Cheat uses advanced Git tools to safely rewrite repository history:

1. **Bare Clone**: Creates a complete bare clone of the source repository
2. **History Rewriting**: Uses git-filter-repo to modify commit authorship and messages
3. **Date Randomization**: Employs git filter-branch to redistribute commit timestamps
4. **Safe Transfer**: Pushes the modified repository to the new location using --mirror
5. **Cleanup**: Removes temporary files and clones

## Advanced Features

### Date Randomization Algorithm
- Generates random timestamps within your specified date range
- Maintains chronological order of commits
- Distributes commits evenly across the time period
- Preserves relative timing relationships where possible

### Message Replacement Engine
- Supports multiple text replacements in a single operation
- Case-sensitive pattern matching
- Handles special characters and encoding properly
- Preserves commit message structure and formatting

## Troubleshooting

### Common Issues

**git-filter-repo not found**
- The script attempts automatic installation
- If it fails, manually install: `pip install --user git-filter-repo`
- Ensure `~/.local/bin` is in your PATH

**Permission denied during push**
- Verify you have write access to the destination repository
- Check that SSH keys are properly configured (for SSH URLs)
- Ensure the destination repository exists and is empty

**Date format errors**
- Use YYYY-MM-DD format exactly (e.g., 2023-01-01)
- Start date must be before end date
- Avoid dates far in the future

**Large repository handling**
- The tool handles repositories of any size
- Processing time scales with commit count
- Monitor disk space for very large repositories

### Error Recovery

If the script fails midway:
1. Check the error message for specific guidance
2. Remove any temporary `.git` directories created
3. Ensure all prerequisites are met
4. Try running the script again

## Security Considerations

- **Backup Important Data**: Always backup your original repository
- **Review Changes**: Verify the transfer completed successfully
- **Access Control**: Ensure proper permissions on both repositories
- **Sensitive Data**: Be cautious when modifying commit messages containing sensitive information

## Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - see LICENSE file for details

## Support

If you encounter issues or have questions:
- Check the troubleshooting section above
- Open an issue on GitHub
- Review the git-filter-repo documentation for advanced usage

---

⭐ **Star this repository** if Git-Cheat helped you clean up your Git history!