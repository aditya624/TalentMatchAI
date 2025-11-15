import streamlit as st

from tamatai.chain.match import Match


@st.cache_resource(show_spinner=False)
def load_match() -> Match:
    return Match()


def main() -> None:
    st.set_page_config(page_title="TalentMatchAI", page_icon="🤝")
    st.title("TalentMatchAI Matcher")
    st.write("Upload a job post image and one or more CV files to run the matcher.")

    with st.form("match-form"):
        job_post_file = st.file_uploader(
            "Upload job post image",
            type=["png", "jpg", "jpeg", "bmp", "gif"],
            accept_multiple_files=False,
            help="Supported formats: PNG, JPG, JPEG, BMP, GIF"
        )
        cv_files = st.file_uploader(
            "Upload CV files",
            type=["pdf"],
            accept_multiple_files=True,
            help="You can upload one or more PDF CV files"
        )
        submit = st.form_submit_button("Process")

    if submit:
        if job_post_file is None:
            st.error("Please upload a job post image before processing.")
            return
        if not cv_files:
            st.error("Please upload at least one CV file before processing.")
            return

        job_post_bytes = job_post_file.getvalue()
        cv_bytes_list = [cv_file.getvalue() for cv_file in cv_files]

        if not job_post_bytes:
            st.error("Uploaded job post file is empty.")
            return
        if any(not cv_bytes for cv_bytes in cv_bytes_list):
            st.error("One or more uploaded CV files are empty.")
            return

        st.info("Processing files. This may take a moment...")
        matcher = load_match()
        try:
            results = matcher.bulk(job_post_bytes, cv_bytes_list)
        except Exception as exc:  # noqa: BLE001 - Surface errors to the UI
            st.error(f"An error occurred while processing the files: {exc}")
            return

        st.success("Processing completed.")
        for idx, result in enumerate(results, start=1):
            st.subheader(f"Result for CV #{idx}")
            st.json(result)


if __name__ == "__main__":
    main()
