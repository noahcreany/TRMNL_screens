import matplotlib.font_manager as fm

# Get a sorted list of unique font names
font_names = sorted(set(f.name for f in fm.fontManager.ttflist))

print("--- Available Matplotlib Fonts ---")
for name in font_names:
    print(name)
print("---------------------------------")