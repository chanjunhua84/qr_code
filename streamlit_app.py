import streamlit as st

# Dictionary of letters with clear structure
letters = {
    "letter1": {
        "title": "CPF Matched Retirement Savings Scheme Notice",
        "content": """
        Central Provident Fund Board
        238B Thomson Road
        #08-00 Tower B Novena Square
        Singapore 307685

        11 March 2025

        Mr Peter Sim
        Block 123 Tampines Street 11
        #08-234
        Singapore 521123

        Dear Mr Sim,

        We are pleased to inform you about the CPF Matched Retirement Savings Scheme (MRSS), which aims to help seniors build their retirement savings.

        Under this scheme, the Government will match every dollar of cash top-up made to your CPF Retirement Account, up to $3,000 per year. This means if you contribute $3,000 to your Retirement Account in a calendar year, you will receive an additional $3,000 from the Government.

        To be eligible, you must:
        - Be aged 55 to 70 years old
        - Have CPF Retirement Account savings below the Basic Retirement Sum
        - Have an average monthly income not exceeding $4,000
        - Own property with an annual value not exceeding $13,000

        The matching will be automatically credited to your Retirement Account by the Government in the following year after your cash top-up.

        For more information or assistance, please:
        - Visit www.cpf.gov.sg
        - Call 1800-227-1188
        - Visit any CPF Service Centre

        Thank you for your attention to this matter.

        Yours sincerely,

        Mary Lim
        Director
        Retirement Savings Department
        CPF Board
        """,
        "level": "Official"
    },
    "letter2": {
        "title": "Budget 2025 Benefits Notification",
        "content": """
        Ministry of Finance
        100 High Street
        #10-01 The Treasury
        Singapore 179434

        11 March 2025

        Ms Sandra Tan
        Block 456 Serangoon Avenue 3
        #15-432
        Singapore 550456

        Dear Ms Tan,

        RE: Your Budget 2025 Benefits

        We are writing to inform you about your eligibility for various support measures under Budget 2025.

        Based on your assessments for Year of Assessment 2024, you qualify for:

        1. Cost-of-Living Special Payment
           - One-off cash payment of $800
           - To be credited to your bank account by April 2025

        2. CDC Vouchers
           - $500 worth of vouchers
           - Digital vouchers will be available via your Singpass app
           - Can be used at participating heartland merchants and supermarkets

        3. GST Assurance Package
           - Additional $300 cash payment
           - To be disbursed in July 2025

        To receive these benefits:
        - Ensure your bank account details are updated on your Singpass app
        - Link your CDC Vouchers via go.gov.sg/cdcv
        - No action required for GST Assurance Package

        For more information about Budget 2025 benefits:
        - Visit www.singaporebudget.gov.sg
        - Call 1800-222-2888
        - Email budget2025@mof.gov.sg

        Thank you for your continued support for Singapore's progress.

        Yours sincerely,

        James Wong
        Director
        Budget Policy Division
        Ministry of Finance
        """,
        "level": "Official"
    }
}

def get_letter_content(letter_id):
    """
    Get the content of a letter based on its ID
    
    Args:
        letter_id (str): The ID of the letter
        
    Returns:
        tuple: (title, content) if letter exists, (None, None) if it doesn't
    """
    if letter_id and letter_id in letters:
        letter = letters[letter_id]
        return letter["title"], letter["content"]
    return None, None

def main():
    st.title("Letter Reader")
    
    # Get query parameters
    query_params = st.experimental_get_query_params()
    
    # Get letter ID from parameters
    letter_id = None
    if 'letter' in query_params:
        letter_id = query_params['letter'][0]

    # Store content in variables
    title, content = get_letter_content(letter_id)
    
    # Display letter based on stored content
    if title and content:
        st.header(title)
        st.markdown(content)
        
        # Store in session state for later use
        st.session_state['current_title'] = title
        st.session_state['current_content'] = content
        
    else:
        st.info("Please scan a valid letter QR code")
        st.write("Available letters:", list(letters.keys()))

if __name__ == "__main__":
    main()
