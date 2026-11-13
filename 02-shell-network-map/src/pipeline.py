"""Run the whole analysis end to end:  python src/pipeline.py

Order matters - each step reads the previous step's files.
"""
import time

import build_subset
import screening
import review
import analysis
import case_study
import visualize

STEPS = [
    ("1. Cut the Cyprus corridor out of ICIJ data", build_subset.main),
    ("2. Screen names against OpenSanctions", screening.screen),
    ("2b. Apply analyst dispositions", review.main),
    ("3. Graph analytics + red flags", analysis.main),
    ("4. Vassiliades/Ledra case study", case_study.main),
    ("5. Interactive maps", visualize.main),
]

if __name__ == "__main__":
    t0 = time.time()
    for title, fn in STEPS:
        print(f"\n=== {title} ===")
        fn()
    print(f"\nDone in {time.time() - t0:.0f}s. See outputs/.")
