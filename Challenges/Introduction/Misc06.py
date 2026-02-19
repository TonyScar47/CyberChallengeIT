import exrex
import re
import sys

# Colors for a pro terminal look
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def solve_regex_challenge(regex_pattern):
    
    # 1. Cleaning: remove slashes, spaces, and potential hidden chars
    clean_pattern = regex_pattern.strip().strip('/')
    
    print(f"\n[*] Analyzing Regex: {YELLOW}{clean_pattern}{RESET}")
    
    try:
        # 2. Generation loop: sometimes exrex generates non-printable chars 
        # that fail validation. We try until we get a perfect match.
        for _ in range(10):
            generated = exrex.getone(clean_pattern)
            
            # 3. Use re.match with the original pattern logic
            if re.match(clean_pattern, generated):
                print(f"{GREEN}[+] Success! String found:{RESET}")
                print(f"\n{generated}\n")
                return
        
        print(f"{RED}[-] Warning: Internal validation failed after 10 attempts.{RESET}")
        print(f"Try to copy this one anyway: {generated}")

    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

if __name__ == "__main__":
    print(f"{YELLOW}========================================={RESET}")
    print(f"{YELLOW}     REGEX SOLVER - CyberChallenge       {RESET}")
    print(f"{YELLOW}========================================={RESET}")
    
    try:
        target_regex = input("\nPaste the regex pattern: ").strip()
        if not target_regex:
            print(f"{RED}Empty input!{RESET}")
            sys.exit(1)
        solve_regex_challenge(target_regex)
    except KeyboardInterrupt:
        print("\nAborted.")
