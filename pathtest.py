import pathlib 

skills_dir = pathlib.Path(__file__)
print(skills_dir)
skills_dir = pathlib.Path(__file__).parent
print(skills_dir)
skills_dir = pathlib.Path(__file__).parent.joinpath('skills')
print(skills_dir)
skills_dir = pathlib.Path(__file__).parent.joinpath('skills').resolve()
print(skills_dir)

skill_files: list[tuple[str,bytes]] = []
for path in sorted(skills_dir.rglob('*')):
    if not path.is_file(): continue
    print(path)
    rel = path.resolve().relative_to(skills_dir)
    print(rel)
    skill_files.append((str(rel), path.read_bytes()))