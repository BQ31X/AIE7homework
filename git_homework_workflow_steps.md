# 🧭 Git Homework Workflow 

I have frequently seen during office hours someone who is in **Git hell**. 
I, too, have struggled with Git — but I refuse to let it _git_ the better of me.

I hope most folks have sorted out their git issues by now. For anyone who has not, I humbly offer this workflow. 

There's lots of ways to manage your Git workflow. This is what is working for me.
If you follow it _assiduously_, it should keep you out of trouble. 

This is by no means a comprehensive guide. It is very specific to our homework repo setup, and is pretty simple, since it only ever uses these 7 GIT commands:

```
git checkout, git branch, git status, git pull, git add, git commit, git push
```

**Note:** This workflow assumes you have already cloned the AIE7 homework repo and configured the `upstream` remote.  
If you haven’t done that yet, check out this [Git Setup Guide](https://github.com/BQ31X/Revamped-AI-Engineer-Challenge/blob/main/docs/GIT_SETUP.md) or ask a peer supporter for help.


---


## 🪜Workflow Steps


## 🛫At the beginning of each session

#### git checkout main

**Why:**  to get on the right branch

**Sample Output:**
```bash
Switched to branch 'main'
```

---
#### git status

**Why:**  to confirm that there aren’t any changes pending

**Sample Output:**
```bash
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---
#### git pull upstream main

**Why:**  to get the latest code from the AIM repo onto

**Sample Output:**
```bash
From https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge
 * branch            main       -> FETCH_HEAD
Updating 3a7d5f1..7b9c4e2
Fast-forward
 README.md       \| 12 ++++++++++++
 docs/setup.md   \| 45 +++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 57 insertions(+)
 create mode 100644 docs/setup.md
```

---
#### git checkout -b sXX-assignment

**Why:**  to create a new branch for current assignment 
(XX = current session number)

**Sample Output:**
```bash
Switched to a new branch 'sXX-assignment'
```

---

## 🛠️While working on homework

#### git checkout sXX-assignment

**Why:**  to get on the branch for whichever homework you are working on

**Sample Output:**
```bash
On branch sXX-assignment
```

---
#### git status

**Why:**  to see what files have changed since your last commit

**Sample Output:**
```bash
On branch sXX-assignment
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   DataRepository

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
  (commit or discard the untracked or modified content in submodules)
        modified:   DataRepository (untracked content)

```

---
#### git add .

**Why:** to ‘stage’ any untracked changes in the current branch

**Sample Output:**
```bash
(no output)
```

---
#### git commit -m “describe your latest change”

**Why:** save early, save often

**Sample Output:**
```bash
[sXX-assignment abc1234] describe your latest change
 2 files changed, 14 insertions(+), 2 deletions(-)
```

---

## 🏁When you finish your homework

#### git push origin sXX-assignment

**Why:**  this makes your work available to graders, and also serves as a backup

**Sample Output:**
```bash
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1.23 KiB \| 1.23 MiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
remote: 
remote: Create a pull request for 'sXX-assignment' on GitHub by visiting:
remote:      https://github.com/<your-username>/The-AI-Engineer-Challenge/pull/new/sXX-assignment
remote: 
To github.com:<your-username>/The-AI-Engineer-Challenge.git
 * [new branch]      sXX-assignment -> sXX-assignment
```

---
## 🔒Rules to Keep You Safe

### 1. Don’t mess with `main`

Never merge, commit, or make changes in your `main` branch.  
The only commands you should need to do with main are:

- `git checkout main`
- `git pull upstream main`

If you think you need to type any other command with the word `main` in it — **stop and git help** from a peer supporter.

---

### 2. When in doubt or things seem missing:

You’re probably just on the wrong branch. Here's your recovery sequence:

1. Don't Panic
2. Make sure you're on the right branch
3. Quit your IDE completely (Cursor, VS Code, etc.)
4. Reopen the IDE

If the file or change is still missing… now you can panic. 
Or better yet: **git help from a peer supporter.**

---
## 🤖❌P.S. Don't trust ChatGPT

> 🚫 **A note on using ChatGPT for Git help**  
> ChatGPT is a powerful tool, but it struggles with Git — especially when you're already in trouble. If you're stuck, it's likely because the repo state is unclear or inconsistent, and GPT doesn't have the full picture. It tends to over-engineer "solutions" that make things worse.  
> **If you're in Git hell, don't get in deeper — ask a peer supporter.**


