from langchain.agents import create_agent
from deepagents.backends import StateBackend,FilesystemBackend
from deepagents.middleware import FilesystemMiddleware,SkillsMiddleware
import csv
import pathlib
import io

backend = FilesystemBackend(root_dir=".",virtual_mode=True)

skills_dir = pathlib.Path(__file__).parent.joinpath("skills")
skill_files:list[tuple[str,bytes]] = []
for path in sorted(skills_dir.rglob("*")):
    if not path.is_file():continue
    skill_files.append((str(path),path.read_bytes()))


agent = create_agent(
    model="deepseek:deepseek-flash",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend),
                SkillsMiddleware(backend=backend,sources=['/skills/'])],
)

rows = [
    ["Date", "Product", "Units", "Revenue"],
    ["2025-08-01", "Widget A", 10, 250],
    ["2025-08-02", "Widget B", 5, 125],
    ["2025-08-03", "Widget A", 7, 175],
    ["2025-08-04", "Widget C", 3, 90],
]
buf = io.StringIO()
csv.writer(buf).writerows(rows)
with open("sales.csv","w",encoding="utf-8") as f:
    f.write(buf.getvalue())

upload_stream = agent.stream_events(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "读取 /sales.csv，并用一句话按产品汇总总收入。"
                    "不要运行 shell 命令。"
                ),
            }
        ]
    },
    version="v3",
    config={"recursion_limit": 8},
)
for item in upload_stream.messages:
    print(item.text)
upload_stream.output

