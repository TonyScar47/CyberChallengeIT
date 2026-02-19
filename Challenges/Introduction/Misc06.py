import exrex
import re

# Define colors for better terminal output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def solve_regex_challenge(regex_pattern):
    """
    Takes a regex pattern and generates a valid matching string.
    """
    print(f"\n[*] Analyzing Regex: {regex_pattern}")
    
    # Clean the regex by removing common web delimiters /^ and $/ 
    clean_pattern = regex_pattern.strip('/')
    
    try:
        # Generate one random string that matches the pattern
        generated_string = exrex.getone(clean_pattern)
        
        # Double-check the result using the standard re library
        if re.match(clean_pattern, generated_string):
            print(f"{GREEN}[+] Success! Generated valid string:{RESET}")
            print(f"{generated_string}")
            return generated_string
        else:
            print(f"{RED}[-] Warning: Generated string failed internal validation.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Regex Error: {e}{RESET}")

# --- MAIN INTERACTIVE LOOP ---
if __name__ == "__main__":
    print("=========================================")
    print("     REGEX SOLVER - CyberChallenge       ")
    print("=========================================")
    
    target_regex = input("Paste the regex pattern: ").strip()
    solve_regex_challenge(target_regex)

# --- ./venv/bin/python Challenges/Introduction/Misc06.py ---