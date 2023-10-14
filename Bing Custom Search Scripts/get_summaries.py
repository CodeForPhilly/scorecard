import pandas as pd
from helpers import get_webpage_text, GPT_Summary

output_df = pd.read_csv("output.csv")

#Update Ouput with GPT Summary
for i,url in enumerate(output_df["URL"]):

    webpage_text = get_webpage_text(url)

    # with open(f"{i}.txt","w") as f:
    #     f.write(webpage_text)

    output_df["GPT-4 Summary"] = GPT_Summary(webpage_text)

output_df.to_csv("output_with_gpt.csv")