import os

#stage = os.environ["STAGE"].upper()

stage = os.getenv("STAGE", default="dev").upper()

output = f"We are running in {stage}"

if stage.startswith("PROD"):
    output = "DANGER!!! - " + output


print(output)