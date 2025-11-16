import streamlit as st

from tamatai.agent.match import Match


@st.cache_resource(show_spinner=False)
def load_match() -> Match:
    return Match()


def _render_header() -> None:
    st.set_page_config(
        page_title="TalentMatchAI",
        page_icon="🤝",
        layout="wide",
    )

    st.markdown(
        """
        <style>
            .tm-card {
                background-color: #ffffff;
                border-radius: 1rem;
                padding: 1.5rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border: 1px solid #f0f2f6;
            }
            .tm-subtitle {
                color: #5c6b7a;
                font-size: 1rem;
                margin-bottom: 0.5rem;
            }
            .tm-section-title {
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #0f4c81;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tm-card" style="margin-bottom: 1.5rem;">
            <h1 style="margin-bottom:0.2rem;">TalentMatchAI Matcher</h1>
            <p class="tm-subtitle">
                Upload job descriptions and candidate CVs to receive matching results that are well
                organized and easy to review.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    _render_header()

    upload_col1, upload_col2 = st.columns(2, gap="large")
    with upload_col1:
        st.markdown("<div class='tm-card'>", unsafe_allow_html=True)
        st.markdown("<p class='tm-section-title'>Job Post PDF</p>", unsafe_allow_html=True)
        st.caption("Upload the job description in PDF format")
        job_post_file = st.file_uploader(
            "Upload job post PDF",
            type=["pdf"],
            accept_multiple_files=False,
            help="Only PDF job posts are supported"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with upload_col2:
        st.markdown("<div class='tm-card'>", unsafe_allow_html=True)
        st.markdown("<p class='tm-section-title'>Candidate CVs</p>", unsafe_allow_html=True)
        st.caption("You can add multiple CVs at once")
        cv_files = st.file_uploader(
            "Upload CV files",
            type=["pdf"],
            accept_multiple_files=True,
            help="You can upload one or more PDF CV files"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='tm-card'>", unsafe_allow_html=True)
    submit = st.button("🚀 Run Matching", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    job_post_bytes = None
    if job_post_file is not None:
        job_post_bytes = job_post_file.getvalue()
        if job_post_bytes:
            with st.expander("Preview Job Post", expanded=False):
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

        with st.status("Processing documents...", expanded=True) as status:
            st.write("Initializing the matching engine")
            matcher = load_match()
            st.write("Analyzing candidate CVs")
            results = matcher.bulk(job_post_bytes, cv_bytes_list)
            status.update(label="Completed", state="complete", expanded=False)

        sorted_results = sorted(
            results,
            key=lambda result: result.get("score"),
            reverse=True,
        )

        st.success("Matching complete. Here is the summary.")

        if sorted_results:
            best_score = sorted_results[0].get("score", 0)
            metrics = st.columns(3)
            metrics[0].metric("CV Count", len(sorted_results))
            metrics[1].metric("Top Score", f"{best_score:.2f}" if isinstance(best_score, (int, float)) else best_score)
            metrics[2].metric("Job Post", job_post_file.name if job_post_file else "-" )

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

        st.markdown("### Matching Details")
        st.dataframe(table_rows, use_container_width=True)


if __name__ == "__main__":
    main()
