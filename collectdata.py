import os, cleantext, io, re;
lines = "" 
i = 0
for channel in os.listdir("discord_data/messages"):
    if channel == "index.json": continue
    print((i := i + 1))
    with open(f"discord_data/messages/{channel}/messages.csv", encoding="utf8") as f:
        cleanf = io.StringIO(cleantext.clean(f.read(), fix_unicode=True, to_ascii=True, lower=True, no_urls=True, replace_with_url="", lang="en"))
        text = [tx[52:-1] for tx in cleanf.read().splitlines()[1:]]
        for row in text[::-1]:
            if row and row != ",":
                if row[-1] == ",": row = row[:-1]
                #lines += row + [". ", " "][row[-1] in {".", ",", "!", "?"}]
                lines += f"{row} "

lines = re.sub(r"<@!?.{0,25}?>", "", lines)
lines = re.sub(r"<.{0,2}:.*?>", "", lines)
lines = re.sub(r"<#.{0,25}>", "", lines)
lines = re.sub(r"<.{0,3}\d{0,25}>", "", lines)
lines = re.sub(r":.{0,20}:", "", lines)
lines = re.sub(r"(<url>|[\@\:\*\|\[\]\/\\])", "", lines)
open("messages.txt", "w", encoding="utf8").write(lines)

