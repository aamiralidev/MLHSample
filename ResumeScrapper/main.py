from extractors import EnhanCVExtractor ,ResumeExampleExtractor ,ResumeIOExtractor ,ResumeBuilderExtractor ,ResumeGeniusExtractor ,ZetyExtractor

if __name__ == "__main__":
    with_resumes = [ResumeBuilderExtractor, ResumeGeniusExtractor, ZetyExtractor]
    only_categories = [EnhanCVExtractor, ResumeExampleExtractor, ResumeIOExtractor]

    for extractor in only_categories:
        rexec = extractor()
        print(extractor.__class__.__name__)
        print(rexec.extract_resume_categories())

    for extractor in with_resumes:
        rexec = extractor()
        print(rexec.extract_resume_categories())