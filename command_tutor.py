#!/usr/bin/python

import random
import difflib
import os
import time

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def clear_screen():
    os.system("clear")

def header():
    print(CYAN + "="*64)
    print("      📚 Interactive Command Tutor — ETA Team ")
    print("="*64 + RESET)

def normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())

def fuzzy_similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()

questions = [
    {"question": "List files in the current directory.", "answer": "ls", "keywords": ["ls", "list"], "topic": "Navigation"},
    {"question": "Change directory to /etc.", "answer": "cd /etc", "keywords": ["cd /etc", "cd etc", "cd"], "topic": "Navigation"},
    {"question": "Print the current working directory.", "answer": "pwd", "keywords": ["pwd", "print working directory"], "topic": "Navigation"},
    {"question": "Show hidden files in the directory.", "answer": "ls -a", "keywords": ["ls -a", "ls -la", "ls -al", "hidden"], "topic": "Navigation"},
    {"question": "Create an empty file named 'notes.txt'.", "answer": "touch notes.txt", "keywords": ["touch notes.txt", "touch"], "topic": "File Manipulation"},
    {"question": "Copy a file 'a.txt' to 'b.txt'.", "answer": "cp a.txt b.txt", "keywords": ["cp a.txt b.txt", "cp a b"], "topic": "File Manipulation"},
    {"question": "Move or rename file 'old' to 'new'.", "answer": "mv old new", "keywords": ["mv old new", "mv"], "topic": "File Manipulation"},
    {"question": "Remove the file 'temp.txt'.", "answer": "rm temp.txt", "keywords": ["rm temp.txt", "rm"], "topic": "File Manipulation"},
    {"question": "Show the first 10 lines of a file 'log.txt'.", "answer": "head log.txt", "keywords": ["head log.txt", "head"], "topic": "Viewing Files"},
    {"question": "Show the last 10 lines of a file 'log.txt'.", "answer": "tail log.txt", "keywords": ["tail log.txt", "tail"], "topic": "Viewing Files"},
    {"question": "View a file page by page (allow scrolling).", "answer": "less file", "keywords": ["less", "more", "less file", "more file"], "topic": "Viewing Files"},
    {"question": "Search for 'error' inside files.", "answer": "grep error", "keywords": ["grep error", "grep"], "topic": "Text Processing"},
    {"question": "Count lines, words and characters in a file.", "answer": "wc filename", "keywords": ["wc", "wc filename", "wc -l"], "topic": "Text Processing"},
    {"question": "Sort the lines of 'data.txt' alphabetically.", "answer": "sort data.txt", "keywords": ["sort", "sort data.txt"], "topic": "Text Processing"},
    {"question": "Remove adjacent duplicate lines from a file.", "answer": "uniq", "keywords": ["uniq", "sort -u"], "topic": "Text Processing"},
    {"question": "Display running processes.", "answer": "ps aux", "keywords": ["ps aux", "ps -ef", "ps"], "topic": "Processes"},
    {"question": "Kill a process with PID 1234.", "answer": "kill 1234", "keywords": ["kill 1234", "kill"], "topic": "Processes"},
    {"question": "Force kill a process (signal 9) with PID 1234.", "answer": "kill -9 1234", "keywords": ["kill -9 1234", "kill -9"], "topic": "Processes"},
    {"question": "Run a command in background.", "answer": "somecommand &", "keywords": ["&", "background", "somecommand &"], "topic": "Processes"},
    {"question": "Add a new user called 'alice'.", "answer": "sudo adduser alice", "keywords": ["adduser alice", "useradd alice", "adduser"], "topic": "Users & Permissions"},
    {"question": "Remove a user 'bob'.", "answer": "sudo deluser bob", "keywords": ["deluser bob", "userdel bob"], "topic": "Users & Permissions"},
    {"question": "Change file permissions to rwxr-xr-- (octal 754).", "answer": "chmod 754 file", "keywords": ["chmod 754", "chmod"], "topic": "Users & Permissions"},
    {"question": "Run a command as root.", "answer": "sudo command", "keywords": ["sudo", "su -c", "run as root"], "topic": "Users & Permissions"},
    {"question": "Check network connectivity to 8.8.8.8.", "answer": "ping 8.8.8.8", "keywords": ["ping 8.8.8.8", "ping"], "topic": "Networking"},
    {"question": "Show IP address information (legacy command).", "answer": "ifconfig", "keywords": ["ifconfig", "ip addr"], "topic": "Networking"},
    {"question": "Show IP address using iproute2 tool.", "answer": "ip addr", "keywords": ["ip addr", "ip a"], "topic": "Networking"},
    {"question": "Check DNS resolution for example.com.", "answer": "nslookup example.com", "keywords": ["nslookup", "dig example.com", "dig"], "topic": "Networking"},
    {"question": "Create a tar.gz archive of folder 'project'.", "answer": "tar -czvf project.tar.gz project", "keywords": ["tar -czvf", "tar -czf", "tar"], "topic": "Archiving"},
    {"question": "Extract a tar.gz file named backup.tar.gz.", "answer": "tar -xzvf backup.tar.gz", "keywords": ["tar -xzvf", "tar -xzf", "tar -x"], "topic": "Archiving"},
    {"question": "Create a zip archive of 'folder'.", "answer": "zip -r folder.zip folder", "keywords": ["zip -r", "zip folder.zip"], "topic": "Archiving"},
    {"question": "Install package 'curl' using apt.", "answer": "sudo apt-get install curl", "keywords": ["apt-get install curl", "apt install curl", "apt install"], "topic": "Software Management"},
    {"question": "Update package lists (apt).", "answer": "sudo apt-get update", "keywords": ["apt-get update", "apt update"], "topic": "Software Management"},
    {"question": "Schedule a one-time job with 'at' for 2pm.", "answer": "at 14:00", "keywords": ["at 14:00", "at"], "topic": "Scheduling"},
    {"question": "Show current date and time.", "answer": "date", "keywords": ["date"], "topic": "Scheduling"},
    {"question": "Open or edit a file with nano.", "answer": "nano file", "keywords": ["nano", "vi", "vim"], "topic": "Editors"},
    {"question": "Show file type / magic info.", "answer": "file filename", "keywords": ["file filename", "file"], "topic": "Editors"},
    {"question": "Redirect output of ls into out.txt.", "answer": "ls > out.txt", "keywords": ["> out.txt", "ls > out.txt", "redirect"], "topic": "Shell & Redirection"},
    {"question": "Pipe output of ls to grep 'py'.", "answer": "ls | grep py", "keywords": ["| grep", "ls | grep"], "topic": "Shell & Redirection"},
    {"question": "Show your command history.", "answer": "history", "keywords": ["history"], "topic": "Shell & Redirection"},
    {"question": "Show disk free space (human readable).", "answer": "df -h", "keywords": ["df -h", "df"], "topic": "Disk & Storage"},
    {"question": "Show disk usage of current directory (human readable).", "answer": "du -sh .", "keywords": ["du -sh", "du -sh ."], "topic": "Disk & Storage"},
    {"question": "List block devices / partitions.", "answer": "fdisk -l", "keywords": ["fdisk -l", "lsblk"], "topic": "Disk & Storage"},
]

topics = sorted({q["topic"] for q in questions})

def evaluate_answer(student_answer: str, correct_answer: str, keywords: list) -> float:
    s = normalize(student_answer)
    correct = normalize(correct_answer)
    if s == correct:
        return 1.0
    for kw in keywords:
        if kw in s or s in kw:
            return 0.5
    if fuzzy_similarity(s, correct) >= 0.65:
        return 0.5
    for kw in keywords:
        if fuzzy_similarity(s, normalize(kw)) >= 0.7:
            return 0.5
    return 0.0

def run_quiz(num_questions=10):
    clear_screen()
    header()
    print(YELLOW + f"Random Quiz — {num_questions} questions\n" + RESET)
    selected = random.sample(questions, k=num_questions)
    total_score = 0.0
    topic_mistakes = {t: 0 for t in topics}
    wrong_details = []

    for idx, q in enumerate(selected, start=1):
        print(CYAN + f"Q{idx}. {q['question']}" + RESET)
        ans = input("Your answer: ").strip()
        score = evaluate_answer(ans, q["answer"], q["keywords"])
        if score == 1.0:
            print(GREEN + "✅ Correct (+1.0)\n" + RESET)
        elif score == 0.5:
            print(YELLOW + f"➖ Partially correct (+0.5) — expected: {q['answer']}\n" + RESET)
            topic_mistakes[q["topic"]] += 1
            wrong_details.append((q["question"], ans, q["answer"], 0.5, q["topic"]))
        else:
            print(RED + f"❌ Wrong (0.0) — expected: {q['answer']}\n" + RESET)
            topic_mistakes[q["topic"]] += 1
            wrong_details.append((q["question"], ans, q["answer"], 0.0, q["topic"]))
        total_score += score
        time.sleep(0.25)

    clear_screen()
    header()
    print(YELLOW + f"Quiz finished — Score: {total_score:.1f} / {num_questions}" + RESET)
    print("-"*64)
    weak = [t for t, m in topic_mistakes.items() if m >= 2]
    medium = [t for t, m in topic_mistakes.items() if m == 1]
    strong = [t for t, m in topic_mistakes.items() if m == 0]

    print(YELLOW + "\n📌 Personalized Study Recommendations:\n" + RESET)
    if weak:
        print(RED + "🔴 Strong revision needed in:" + RESET)
        for t in weak: print(f"- {t}")
    if medium:
        print(YELLOW + "\n🟡 Some revision recommended in:" + RESET)
        for t in medium: print(f"- {t}")
    if strong:
        print(GREEN + "\n🟢 Strong areas (keep practicing):" + RESET)
        for t in strong: print(f"- {t}")

    suggestions = {
        "Navigation": "ls, cd, pwd, ls -a",
        "File Manipulation": "touch, cp, mv, rm",
        "Viewing Files": "head, tail, less, cat",
        "Text Processing": "grep, wc, sort, uniq, sed, awk",
        "Processes": "ps, top, kill, & (background)",
        "Users & Permissions": "adduser, deluser, chmod, sudo",
        "Networking": "ping, ifconfig / ip addr, nslookup, dig",
        "Archiving": "tar -czvf, tar -xzvf, zip",
        "Software Management": "apt-get update/install",
        "Scheduling": "at, cron, date",
        "Editors": "nano, vi/vim",
        "Shell & Redirection": ">, >>, |, history",
        "Disk & Storage": "df -h, du -sh, fdisk -l",
    }
    for t in (weak + medium):
        if t in suggestions: print(f"- {t}: {suggestions[t]}")

    if wrong_details:
        print("\n" + YELLOW + "Questions to review (what you answered vs correct):" + RESET)
        for q_text, student_ans, corr, given, topic in wrong_details:
            print(f"\nTopic: {topic}")
            print(f"Q: {q_text}")
            print(f"Your answer: {student_ans}")
            print(f"Expected: {corr}")
            print(f"Score given: {given}")

    print("\n" + CYAN + "Keep practicing — try another random quiz to get different questions!" + RESET)
    input("\nPress Enter to return to main menu...")

def study_mode():
    clear_screen()
    header()
    print(YELLOW + "STUDY MODE — Commands grouped by topic\n" + RESET)
    grouped = {}
    for q in questions:
        grouped.setdefault(q["topic"], []).append((q["question"], q["answer"]))

    for t in sorted(grouped.keys()):
        print(CYAN + f"\n-- {t} --" + RESET)
        for q_text, ans in grouped[t]:
            print(f"• {q_text}  {GREEN}→ {ans}{RESET}")
        time.sleep(0.08)

    input("\nPress Enter to return to menu...")

def main_menu():
    while True:
        clear_screen()
        header()
        print(YELLOW + "1. Start Random Quiz (10 questions)")
        print("2. Study Mode (view commands)")
        print("3. Exit" + RESET)
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == "1":
            run_quiz(num_questions=10)
        elif choice == "2":
            study_mode()
        elif choice == "3":
            print(GREEN + "\nGood luck and happy practicing! 👋" + RESET)
            break
        else:
            print(RED + "Invalid choice. Try again." + RESET)
            time.sleep(0.8)

if __name__ == "__main__":
    main_menu()
