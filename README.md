# ctf-ultimate-cheat-sheet
The "Capture the Flag Ultimate Cheat Sheet" project compiles commands from existing cheat sheets into a comprehensive resource for CTF challenges. It aims to provide participants with quick access to the most relevant commands and techniques, enhancing their performance in CTF competitions.

Approach:
  - Python Script to extract commands used in CTF Challenges. Website used = nfosecinstitution.com
      - get the name of the CTF Challenge
      - input the name into the URL to get the related challenge
      - extract the HTML 
      - screening of the HTML to get the contents commands
      - Safe the name and commands to an additional file (add)
      - (automatically) select the name of the next CTF Challengen
      - ...
