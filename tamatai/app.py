import streamlit as st

from tamatai.chain.match import Match


@st.cache_resource(show_spinner=False)
def load_match() -> Match:
    return Match()


def main() -> None:
    st.set_page_config(page_title="TalentMatchAI", page_icon="🤝")
    st.title("TalentMatchAI Matcher")
    st.write("Upload a job post PDF and one or more CV files to run the matcher.")

    with st.form("match-form"):
        job_post_file = st.file_uploader(
            "Upload job post PDF",
            type=["pdf"],
            accept_multiple_files=False,
            help="Only PDF job posts are supported"
        )
        cv_files = st.file_uploader(
            "Upload CV files",
            type=["pdf"],
            accept_multiple_files=True,
            help="You can upload one or more PDF CV files"
        )
        submit = st.form_submit_button("Process")

    job_post_bytes = None
    if job_post_file is not None:
        job_post_bytes = job_post_file.getvalue()
        if job_post_bytes:
            st.markdown("#### Job Post Preview")
            st.pdf(job_post_bytes)
        else:
            job_post_bytes = None

    if submit:
        if job_post_bytes is None:
            st.error("Please upload a job post PDF before processing.")
            return
        if not cv_files:
            st.error("Please upload at least one CV file before processing.")
            return

        cv_bytes_list = [cv_file.getvalue() for cv_file in cv_files]

        if not job_post_bytes:
            st.error("Uploaded job post PDF is empty.")
            return
        if any(not cv_bytes for cv_bytes in cv_bytes_list):
            st.error("One or more uploaded CV files are empty.")
            return

        st.info("Processing files. This may take a moment...")
        matcher = load_match()
        results = matcher.bulk(job_post_bytes, cv_bytes_list)

        st.success("Processing completed.")

        sorted_results = sorted(
            results,
            key=lambda result: result.get("score"),
            reverse=True,
        )

        table_rows = []
        for idx, result in enumerate(sorted_results, start=1):
            table_rows.append(
                {
                    "CV #": idx,
                    "Name": result.get("name", "-"),
                    "Role": result.get("role", "-"),
                    "Years of Experience": result.get("year_experience", "-"),
                    "Score": result.get("score", "-"),
                    "Summary": result.get("summary", "-"),
                }
            )

        st.dataframe(table_rows, use_container_width=True)


if __name__ == "__main__":
    main()
