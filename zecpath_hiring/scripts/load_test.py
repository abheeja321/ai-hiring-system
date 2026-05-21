import sys
import time
import concurrent.futures

# Make sure we can import from the main project
sys.path.insert(0, ".")

from zecpath_hiring.ai.parsers.resume_parser import parse_resumes_batch, parse_resume_text
from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline

def run_load_test():
    print("--- Starting System Load Test ---")
    
    # 1. Prepare Mock Data
    job_title = "Senior Backend Engineer"
    job_description = "We are looking for a Senior Backend Engineer with 5+ years of Python and Django experience."
    resumes_payload = [
        {"candidate_name": f"Candidate {i}", "resume_text": "Python, Django backend developer with 6 years experience."}
        for i in range(50)
    ]
    
    # 2. Test Batch Parsing (Threading)
    start_time = time.time()
    parsed_resumes = parse_resumes_batch(resumes_payload, max_workers=20)
    batch_time = time.time() - start_time
    print(f"Batch parsed {len(parsed_resumes)} resumes in: {batch_time:.3f}s")
    
    # 3. Test LRU Cache & Pipeline Concurrency
    structured_job = parse_job_description(job_title, job_description)
    
    start_time = time.time()
    
    def process_pipeline(resume):
        try:
            return run_hiring_pipeline(resume, structured_job)
        except Exception as e:
            return {"error": str(e)}

    # Simulate 50 concurrent pipeline runs
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(process_pipeline, parsed_resumes))
        
    pipeline_time = time.time() - start_time
    print(f"Executed 50 concurrent Hiring Pipelines in: {pipeline_time:.3f}s")
    print(f"Average Pipeline Time / Candidate: {(pipeline_time / 50):.4f}s")
    
    success_count = sum(1 for r in results if "error" not in r)
    print(f"Successful Runs: {success_count} / 50")
    print("--- Load Test Complete ---")

if __name__ == "__main__":
    run_load_test()
