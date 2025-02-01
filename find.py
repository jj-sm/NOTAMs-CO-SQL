import os
import re

def find_imports(directory):
    imports = set()
    pattern = re.compile(r'^\s*(?:import|from) (\S+)')

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        match = pattern.match(line)
                        if match:
                            imports.add(match.group(1).split('.')[0])  # Get base package name

    return sorted(imports)

folder_path = "NIC"  # Change this to your target folder
libs = find_imports(folder_path)
print("\n".join(libs))