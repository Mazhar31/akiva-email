from astrapy import DataAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)

# Collections for session and chat history
General_QA_Collection = db.get_collection("general_qa")
Objection_QA_Collection = db.get_collection("objection_qa")
Retainer_QA_Collection = db.get_collection("retainer_qa")


General_QA_dict = {
     "GA1": ["What is a Trust?",
          "A trust is a estate planning tool that allows you to manage your assets during your lifetime and incpacity, and specify how they should be distributed after your death. Placing your assets in Living Trust will help avoid probate."],
     "GA2": ["What is an Irrevocable Trust?",
          "An Irrevocable Trust is a permanent estate planning tool that can't be easily modified or revoked once established, offering benefits like asset protection and potential tax advantages."],
     "GA3": ["What is a Revocable Trust?",
          "A Revocable Trust is a flexible estate planning tool that allows you to manage your assets during your lifetime and specify how they should be distributed after your death. You can modify or revoke the trust at any time."],
     "GA4": ["What is the difference between an Irrevocable Trust and a Revocable Trust?",
          "The main difference is that a Revocable Trust can be modified or revoked at any time, while an Irrevocable Trust is more permanent and cannot be easily changed once established."],
     "GA5": ["What do you offer or provide?",
          "Through our website, we offer two Living Trust Packages: Revocable & Irrevocable Living Trusts. Plus, for a limited time, your Living Trust Package comes with free documents, like a will & advance directives with each. The two packages offered for basic estate planning. Sophisticared Esate Planning generally requires a custom package. If you need a custom package, our attorney will advise you when you meet with them."],
     "GA8": ["How can a Living Trust help reduce estate taxes?",
          "Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA9": ["How does a Living Trust help avoid probate?",
          "A Living Trust helps avoid probate by facilitating that assets in the trust are transferred directly to beneficiaries, bypassing the often costly, time-consuming and frustratring probate process."],
     "GA10": ["What is the role of a trustee in a trust?",
          "The trustee is responsible for managing the assets in the trust according to the grantor's wishes and for distributing them to the beneficiaries as specified in the trust."],
     "GA11": ["Can a Living Trust protect assets from creditors?",
          "Yes, an Irrevocable Living Trust can protect assets from future creditors. Once assets are transferred into the trust, they are generally protected from future creditors and legal claims."],
     "GA13": ["What is a Charitable Trust?",
          "A Charitable Trust allows the grantor to donate assets to a charitable organization while receiving tax benefits. There are two main types: Charitable Remainder Trusts (CRTs) and Charitable Lead Trusts (CLTs). Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA14": ["What is a Special Needs Trust?",
          "A Special Needs Trust provides for a disabled beneficiary without affecting their eligibility for government benefits like Medicaid or SSI, ensuring access to additional financial resources without losing public assistance."],
     "GA15": ["How can a Testamentary Trust be used?",
          "A Testamentary Trust is created through a will and becomes effective after the grantor's death. It’s often used to manage assets for minor children or beneficiaries who cannot manage the assets themselves. The disadvantage of a Testamentary Trust is that it does not help avoid the probate, which is often costly, time-consuming, and frustrating."],
     "GA16": ["What are the benefits of a Charitable Trust?",
          "Charitable Trusts offer tax deductions for contributions, help reduce estate and income taxes, and allow the grantor to leave a lasting legacy by supporting causes they care about. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet. "],
     "GA17": ["What is an Irrevocable Life Insurance Trust (ILIT)?",
          "An ILIT is a type of irrevocable trust that holds life insurance policies. The proceeds from the life insurance policy are excluded from the taxable estate, reducing estate taxes. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA18": ["Can a Living Trust help with capital gains taxes?",
          "Yes, appreciated assets passed through a Living Trust at death generally receive a step-up in basis which eliminates capital gains taxes on the appreciation accumulated during the grantor's lifetime. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA19": ["How can a Special Needs Trust preserve government benefits for the beneficiary?",
          "A Special Needs Trust is structured so that its assets are not counted toward the beneficiary’s eligibility for government assistance programs like Medicaid and SSI."],
     "GA20": ["What happens to assets in an Irrevocable Living Trust after the grantor’s death?",
          "Assets in an Irrevocable Living Trust bypass probate and are transferred directly to beneficiaries."],
     "GA21": ["Who manages the assets in a Trust?",
          "The assets in a Trust are managed by the appointed trustee. The trustee is responsible for managing and distributing the assets according to the grantor's instructions."],
     "GA22": ["Can a Living Trust help reduce family disputes after death?",
          "Yes, since a Living Trust allows for direct transfer of assets without court involvement, it reduces the chances of disputes among family members over the estate."],
     "GA23": ["What is the difference between a Living Trust and a Testamentary Trust?",
          "A Living Trust is created and effective during the grantor's lifetime allowing assets to bypass probate. A Testamentary Trust is created through a will and only becomes effective after the grantor's death, and must go through probate."],
     "GA26": ["Who can benefit from setting up a Special Needs Trust?",
          "A Special Needs Trust is ideal for individuals who have a disabled beneficiary. It allows the grantor to provide for the beneficiary without risking their eligibility for government programs such as Medicaid or SSI."],
     "GA27": ["What type of control does a grantor retain in a Special Needs Trust?",
          "The grantor can customize the Special Needs Trust to suit the beneficiary’s needs, but the assets placed in the trust are generally managed by a trustee."],
     "GA28": ["What is the main advantage of a Charitable Remainder Trust (CRT)?",
          "A Charitable Remainder Trust allows the grantor or another beneficiary to receive income from the trust for a period, after which the remaining assets go to a charity, offering both income and tax benefits. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA29": ["How does a Charitable Lead Trust (CLT) work?",
          "In a Charitable Lead Trust, the charity receives income from the trust for a set period, and the remaining assets are transferred to other beneficiaries, such as family members, after that period ends. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA30": ["Can a Charitable Trust help with tax planning?",
          "Yes, contributions to Charitable Trusts can qualify for charitable deductions, and they also allow for strategic tax planning, especially in reducing estate and income taxes. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA31": ["What happens to assets in an Irrevocable Living Trust in case of litigation?",
          "Generally speaking, assets in an Irrevocable Living Trust are shielded from future creditors and legal claims because they are considered gifts and are no longer owned by the grantor."],
     "GA32": ["How can Living Trusts save time for beneficiaries?",
          "Living Trusts allow assets to be transferred directly to beneficiaries upon the grantor's death, avoiding the often lengthy, costly, and frustrating probate process that typically occurs with a will."],
     "GA33": ["Can I use a Living Trust to manage my estate while I am alive?",
          "Yes, Living Trusts allow the grantor to manage their estate while they are alive and pass assets smoothly to beneficiaries after death, avoiding probate."],
     "GA34": ["How can a Living Trust help beneficiaries who are minors?",
          "A Living Trust allows you to specify when and how assets are distributed to minors, ensuring responsible management of the assets until the minors are mature enough to handle them."],
     "GA36": ["How can I modify an Irrevocable Living Trust?",
          "Generally, an Irrevocable Living Trust cannot be modified by the grantor once established. However, the grantor can retain some powers, such as allocation percentage ditribution, and changes can sometimes be made if all grantors and all beneficiaries agree or through a court order under certain conditions."],
     "GA37": ["What is the process for setting up a Charitable Trust?",
          "Setting up a Charitable Trust involves defining the trust’s purpose, selecting a trustee, drafting the trust document, and transferring assets into the trust. Legal and tax advisors often assist in ensuring compliance with regulations. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA38": ["What are the benefits of a Charitable Remainder Trust (CRT) for income tax planning?","A Charitable Remainder Trust offers a charitable deduction based on the present value of the remainder interest passing to charity, which can reduce income tax liability. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA39": ["How does a Charitable Lead Trust (CLT) benefit estate planning?",
          "A Charitable Lead Trust provides immediate charitable contributions, with the remainder passing to family members or other beneficiaries, potentially reducing estate and gift taxes. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
    
     "GA40": ["What is Will(Last Will & Testament)?",
          "A will is a legal document that specifies your wishes regarding the distribution of your assets, the care of minor children, and other important matters after your death. A will must be probated in order to take effect. Probate is an often lengthy, costly, and frustrating process involving the Surrogate’s Court."],
     "GA41": ["What are the Components of a Will?",
          "A will has four main components: the Executor, who manages your estate; Beneficiaries, who receive your assets; Specific Bequests, for designated gifts like heirlooms or donations; and the Residuary Estate, which covers any remaining assets not specifically mentioned."],
     "GA42": ["What is the Importance of a Will?",
          "A will is important because it helps ensure that your assets are distributed according to your wishes and during the probate process. Without it, the State laws will determine how assets still in your name are going to be divided, which might not align with your intentions."],

     "GA44": ["Can a Charitable Trust be used to support a specific charity or cause?",
          "Yes, a Charitable Trust can be set up to support a specific charity or cause by directing the trust’s assets or income to that organization or cause. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA45": ["How does a Special Needs Trust impact government benefit eligibility?",
          "A Special Needs Trust is designed to supplement the beneficiary’s government benefits without disqualifying them, ensuring that trust assets are not counted as personal assets."],
     "GA46": ["What are the key features of a Revocable Living Trust?",
          "A Revocable Living Trust allows the grantor to retain control over the trust assets during their lifetime with the ability to modify or revoke the trust. It avoids probate and facilitates the transfer of assets upon the grantor's death."],
     "GA48": ["What is the benefit of using an Irrevocable Trust for asset protection?",
          "An Irrevocable Trust offers strong asset protection because once assets are transferred into the trust, they are generally shielded from future creditors and legal claims against the grantor."],
     "GA58": ["What are the limitations of a charitable lead trust?",
          "Limitations of a Charitable Lead Trust include complex administration, potential high costs, and the requirement to make annual charitable payments, which may impact the trust’s income distribution to other beneficiaries. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA59": ["How does a charitable remainder trust differ from a charitable lead trust?",
          "A Charitable Remainder Trust (CRT) provides income to the grantor or other beneficiaries for a specified period, with the remainder going to charity. A Charitable Lead Trust (CLT) provides immediate income to charity, with the remainder going to beneficiaries. Please note that tax planning is a complex subject beyond the scope of my training. Please discuss this with our attorney when you meet."],
     "GA61": ["What are Advance Directives?",
          "Advance Directives include a Power of Attorney, Living Will, Health Care Proxy, and HIPAA Authorization."],
     "GA62": ["What is a Power of Attorney (also known as a DPOA or POA)?",
          "A Power of Attorney, sometimes called a Durable Power of Attorney when it acts during incapacity, generally allows someone you trust to manage your finances according to your wishes, generally when you are unable to do so. It is a powerful document and should be planned for carefully."],
     "GA63": ["What is a Health Care Proxy (also known as an HCP)?",
          "A Health Care Proxy allows someone you trust to make medical decisions on your behalf in the event that you are unable to do so. You should have frank discussions of your medical desires with the person you appoint as your Health Care Proxy."],
     "GA64": ["What is a Living Will?"
          ,"A Living Will provides direction to your Health Care Proxy and to the Hospital of what your wishes are with respect to end of life decisions should you be in a terminal and vegitative condition."],
     "GA65": ["What is a HIPAA Authorization?",
          "A HIPAA Authorization allows people you designate, other than your Health Care Proxy to access your medical records and speak to doctors. Only your Health Care Proxy is legally allowed to make decisions on your behalf, but the HIPAA Authorization allows family members to get involved in the process."],
     
     "GA67": ["What estate planning packages are offered by NY Estate Law .ai or what services are included in a Living Trust Package?",
        "NY Estate Law .ai offers two packages: the Revocable Trust Package and the Irrevocable Trust Package. For a limited time, both packages come with additional estate planning documents such as a will, durable power of attorney, health care proxy, living will, and HIPAA authorization."], 
   
    "GA68": ["What are the benefits of using NY Estate Law .ai for estate planning? or What are the Benefits of AI Onboarding",
        "NY Estate Law .ai combines the efficiency of AI-powered onboarding with personalized legal service. Clients can save up to 30% by using the AI onboarding process, while still having access to human consultations if needed. The firm also guarantees 100% satisfaction, offering a refund or adjustment to a custom plan if necessary."],


    "GA69": ["What documents are included in the Living Trust Packages offered by NY Estate Law .ai?",
        "The Living Trust Packages include essential estate planning documents such as a Revocable or Irrevocable Living Trust, a will, durable power of attorney, health care proxy, living will, and HIPAA authorization."],


    "GA70": ["How does NY Estate Law .ai ensure customer satisfaction?",
        "NY Estate Law.ai guarantees 100% satisfaction by offering a refund or the option to apply the purchase price toward a custom estate plan if the initial package does not meet your needs after consultation with your NY Estate Plan .ai attorney."],
   
    "GA71": ["How can trusts help avoid probate in New York?",
        "Trusts allow assets to bypass probate by ensuring they are transferred directly to beneficiaries, avoiding the lengthy and costly Surrogate's Court process in New York."],


#    "GA72": ["How does NY Estate Law.ai ensure privacy in estate planning?",
#        "NY Estate Law.ai helps maintain privacy by utilizing trusts, which keep estate matters private and out of public Surrogate's Court records."],


    "GA73": ["What is a Pour Over Will, and why is it important?",
        "A Pour Over Will ensures that any assets not placed in your Living Trust during your lifetime are transferred ('poured over') into your Living Trust upon your death. This does not avoid probate for those assets, so you should make sure all your assets are in your Trust for maximum benefit."],


    "GA74": ["What happens if I want to change my estate plan in the future?",
        "Estate plans can be updated as your life changes. NY Estate Law .ai recommends reviewing your estate plan regularly or after significant life events to ensure it continues to reflect your current wishes."],


    "GA75": ["How do joint ownership and beneficiary designations help avoid probate?",
        "Joint ownership with right of survivorship and beneficiary designations, such as Payable-On-Death (POD) or Transfer-On-Death (TOD) accounts, allow assets to pass directly to the surviving owner or designated beneficiaries, avoiding probate."],


    "GA76": ["What are Payable-On-Death (POD) and Transfer-On-Death (TOD) accounts?",
        "POD and TOD accounts allow you to name beneficiaries who will receive the funds in your bank or investment accounts directly upon your death, bypassing probate and ensuring quick transfer of assets."],


    "GA77": ["What is a Medicaid Asset Protection Trust, and how does it work?",
        "A Medicaid Asset Protection Trust is an irrevocable trust that helps reduce countable assets for Medicaid eligibility purposes while preserving those assets for heirs."],


    "GA78": ["How can a Living Trust help protect my assets from creditors?",
        "An Irrevocable Living Trust can protect your assets from future creditors by transferring ownership out of your personal estate, shielding those assets from legal claims."],


    "GA79": ["What is the Small Estate Affidavit process in New York?",
        "In New York, if an estate is valued below $50,000 (excluding real estate), beneficiaries can use the Small Estate Affidavit process to collect and distribute assets without formal probate."],


    "GA80": ["How can a Standalone Retirement Trust help manage retirement assets?",
        "A Standalone Retirement Trust allows you to manage retirement accounts and offers control over how those assets are distributed, while still avoiding probate for those assets. Very importantly, it also provides protection against your beneficiaries' creditors, which is not something that an inherited retirement account can do."],

     "GA81": ["How does an Irrevocable Life Insurance Trust (ILIT) reduce estate taxes?",
        "An Irrevocable Life Insurance Trust (or ILIT) holds life insurance policies outside your taxable estate, which can help reduce estate taxes by excluding the policy proceeds from estate tax calculations."],


    "GA82": ["What are the key benefits of using a Trust-Based Estate Plan?",
        "A Trust-Based Estate Plan can help avoid probate, provide privacy, reduce family conflicts, protect assets from creditors, and give you control over how your assets are managed and distributed."],


    "GA83": ["How can a trust protect my estate from family conflicts?",
        "A trust can prevent family conflicts by clearly outlining how your assets should be managed and distributed, reducing ambiguity and legal disputes among beneficiaries."],


    "GA84": ["What is the importance of regularly updating my estate plan?",
        "Regular updates ensure your estate plan reflects changes in your family, finances, or the law. NY Estate Law. ai recommends periodic reviews to keep your estate plan aligned with your current wishes."],


    "GA85": ["How does gifting during my lifetime help avoid probate?",
        "Asset you give during your lifetime generally bypass probate. There are numerous disadvantages to giving significant assets during your lifetime. Please discuss this with your NY Estate Law .ai attorney for information specific to your situation."],


    "GA86": ["How can estate planning protect minors?",
        "An estate plan allows you to name guardians for your minor children and create trusts that control how and when assets are distributed, ensuring responsible management for minors until they are ready."],


    "GA87": ["How does a Testamentary Trust differ from a Living Trust?",
        "A Testamentary Trust requires probate because it is created through a will and takes effect after death, while a Living Trust is established during your lifetime and helps avoid probate."],


    "GA88": ["What are the key benefits of avoiding probate in New York?",
        "Avoiding probate saves time, reduces legal fees, protects your family’s privacy, and ensures your estate is managed efficiently without delays from the Surrogate’s Court."],


    "GA89": ["How does NY Estate Law. ai ensure affordable estate planning?",
        "NY Estate Law.ai offers affordable estate planning by utilizing AI onboarding, which reduces costs while still providing personalized legal advice from a genuine attorney."],


    "GA90": ["How do I start the estate planning process with NY Estate Law. ai?",
        "You can start by visiting nyestatelaw.ai to select a package through AI onboarding or schedule a consultation with one of our wonderful human Onboarding Specialists to assist in your estate planning purchase."],


    "GA91": ["What is AI onboarding?",
        "AI onboarding is the process offered by NY Estate Law. ai where you can select an estate planning package online assisted by artificial intelligence (me, AI Kelly). It allows you to efficiently choose between the Revocable Trust Package or Irrevocable Trust Package with transparent pricing and the opportunity to save up to 30% compared to human onboarding. This process is designed to be quick and accessible, providing a convenient way to start your estate planning journey."],


    "GA92": ["What is the difference between a Revocable and an Irrevocable Trust in terms of control?",
        "A Revocable Trust allows you to retain full control over your assets during your lifetime and make changes or revoke the trust at any time. In contrast, an Irrevocable Trust requires you to relinquish control over the assets once they are placed in the trust, offering benefits like asset protection but cannot be easily changed."],


    "GA93": ["What is a Standalone Retirement Trust, and why should I consider one?",
        "A Standalone Retirement Trust is a trust specifically designed to manage retirement accounts like IRAs. It allows you to control how those assets are distributed to beneficiaries and offers protection from your beneficaries' creditors, while also helping avoid probate."],


    "GA94": ["How does NY Estate Law .ai’s AI onboarding save time and money?",
        "The AI onboarding process offered by NY Estate Law.ai streamlines estate planning by assisting you in purchasing your Living Trust Package online. This reduces the need for lengthy in-person, pre-purchase consultations, cutting costs by up to 30% while ensuring efficient estate planning by meeting with your genuine NY Estate Law .ai attorney after you make your purchase."],


    "GA95": ["What is the role of a trustee in an Irrevocable Trust?",
        "In an Irrevocable Trust, the trustee manages the assets according to the terms set by the grantor. Unlike a Revocable Trust, the grantor usually cannot serve as the trustee, and the trustee must act independently to manage and distribute the assets for the beneficiaries."],


    "GA96": ["Can I update my trust if I use the AI onboarding process?",
        "Yes, if you start with the AI onboarding process and you decide after meeting with your NY Estate Law .ai attorney that a different Living Trust Package better suits your needs, you can make the change."],


    "GA97": ["What is the Small Estate Affidavit process in New York, and when can it be used?",
        "The Small Estate Affidavit process is a simplified way to settle an estate in New York when the total value is below $50,000, excluding real estate. It avoids the need for full probate and can be used by heirs to collect and distribute assets more quickly and affordably."],


    "GA98": ["What happens if I die without a will or trust in New York?",
        "If you die without a will or trust in New York, your assets will go through the intestacy process in Surrogate’s Court, where NY State will distribute your estate according to state laws. This can lead to delays, higher costs, frustration, and distributions that may not align with your wishes."],


    "GA99": ["How can a Trust-Based Estate Plan help protect my minor children?",
        "A Trust-Based Estate Plan allows you to name guardians for your minor children and set up trusts that manage their inheritance until they reach maturity. This ensures their financial future is secured and managed responsibly in case something happens to you."],


    "GA100": ["What does it mean to fund a trust, and why is it important?",
        "Funding a trust means transferring your assets, such as real estate, bank accounts, and investments, into the name of the trust. This is essential for the trust to be effective and ensure that those assets bypass probate and are distributed according to your wishes."],


    "GA101": ["What is NY Estate Law. ai?",
        "NY Estate Law.ai is a legal service that combines AI technology with the expertise of genuine human attorneys to provide affordable and efficient estate planning. It offers packages like Revocable and Irrevocable Living Trusts, along with other essential estate planning documents."],


    "GA102": ["Where is NY Estate Law .ai located or what's your address or what's NY Estate Law .ai's address?",
        "NY Estate Law .ai's physical and mailing addresses can be found at the bottom of the website nyestatelaw.ai"],


    "GA103": ["What does 'genuine attorney' mean?",
        "'Genuine attorney' refers to the licensed legal professionals at NY Estate Law. ai who review and customize estate plans to ensure they meet your individual needs. While AI helps streamline the process, the drafting, final review, and legal advice are provided by genuine, qualified attorneys."],


    "GA104": ["What does AI onboarding mean at NY Estate Law. ai?",
        "AI onboarding at NY Estate Law.ai is a process where an AI system, without giving legal advice, answers your questions so you can select the right estate planning package. This allows you to save time and money while still receiving genuine human attorney oversight to confirm your package selection, final review, and legal advice, in line with your individual needs."],


    "GA105": ["What are the working hours for NY Estate Law. ai?",
        "The working hours for humans at NY Estate Law.ai can vary, but are generally 9am to 5pm M-F, excluding certain holidays. However, you can always interact with me, AI Kelley, 24 hours a day, 7 days a week, and even on Holidays. And you can email, schedule appointments, and use our online booking system for consultations with one of our wonderful human Onboarding Specialists."],


    "GA106": ["How do I contact NY Estate Law .ai?",
        "You can contact NY Estate Law .ai by phone at 888-992-7979, by email at Info@nyestatelaw.ai, or visit our website at nyestatelaw.ai."],


#    "GA107": ["What services are included in a Living Trust Package?",
#        "The Living Trust Package includes either a Revocable or Irrevocable Living Trust, a will, durable power of attorney, health care proxy, living will, and HIPAA authorization, ensuring comprehensive #estate planning."],


    "GA108": ["How long does the estate planning process take with NY Estate Law.ai?",
        "The process duration varies depending on individual needs, but the AI onboarding process helps streamline and speed up the initial setup. Final reviews by attorneys typically follow shortly after the onboarding process. Rush service is available in the event of an emergency. Please speak to one of our terrific human Onboarding Specialists if you have a rush need."],


    "GA109": ["What is included in the free consultation?",
        "The free consultation includes an initial discussion with our AI or one of our wonderful human Onboarding Specialists to answer basic questions, without giving legal advice, about our Living Trust and Estate Planning offerings, and assisting you in your purchase, should you decide to proceed."],


    "GA110": ["Can I meet with an attorney in person at NY Estate Law.ai?",
        "Yes, although much of the process can be completed online through AI onboarding, you have the option to meet with an attorney in person if desired. Please contact one of our wonderful human Onboarding Specialists at 888-992-7979 to discuss setting up an appointment with your NY Estate Law .ai attorney."],

    "GA111": ["What is the company name?",
    "The Company's name is NY Estate Law .ai"],

    "GA112": ["What is your name?",
    "My name is AI Kelley. I'm an artificial intelligence."],
    
    "GA113": ["How much does it cost? or How much do trusts cost?",
    "NY Estate Law .ai offers two packages: the Revocable Living Trust Package and the Irrevocable Living Trust Package. For a limited time, both packages come with additional estate planning documents valued at more than $2,500 per person, such as a pour over will, durable power of attorney, health care proxy, living will, and HIPAA authorization. The cost of either package for human Onboarding is $3,995. Compare this to $6,500 for a trust purchased elsewhere. If you take advantage of our AI Onboarding process, you'll save an additional 30%. So, you get the entire Living Trust Package, plus the additional documents, valued at $9,000 - $10,000 for only $2,795. We even offer payment plans. Our transparent, low pricing is just one example of how we're making Estate Planning affordable and accessible for all New Yorkers."],
    
    "GA114": ["What is human Onboarding?",
    "Human Onboarding is our process for assisting you making your Trust Package Purchase through a live human being. You also have the option of AI Onboarding, which can save you an additional 30% off of our already low, transparent Living Trust Package pricing."],

    "GA115": ["What time is it?",
    "The current time depends on where you live, of course. As an AI trained in specific information with respect to NY Estate Law .ai, I do not have access to the current time in my current training current model."],

    "GA116": ["What are the unique advantages of a Trust-Based Estate Plan over a Will?",
    "A Trust-Based Estate Plan helps avoid probate, offers privacy, and allows for efficient asset distribution. Unlike a Will, which goes through probate, a Trust allows assets to be transferred directly to beneficiaries without court involvement."],

    "GA117": ["What are the benefits of avoiding the Surrogate’s Court in New York?",
    "Avoiding the Surrogate’s Court helps speed up the asset distribution process, reduces legal costs, and keeps your estate matters private, as Surrogate’s Court proceedings are public."],

    "GA118": ["Why are the key estate planning documents important before retirement?",
    "The five key estate planning documents—Living Trust, Pour Over Will, Durable Power of Attorney, Health Care Proxy, and Living Will. If you would like to know more details about any of these documents, please feel free to ask."],

    "GA119": ["What happens if I need to update my estate plan after major life changes?",
    "A Revocable Trust can be updated as your circumstances change, such as after a marriage, divorce, or the birth of a child. An Irrevocable Trust is more difficult to modify and typically requires legal guidance."],

    "GA120": ["How can a Trust ensure the responsible management of assets for minors?",
    "A Trust allows you to appoint a trustee to manage and distribute assets for minors until they reach an appropriate age, ensuring financial responsibility."],

    "GA121": ["How does the Trust setup process work with NY Estate Law .ai?",
    "NY Estate Law .ai offers an AI-powered onboarding system for efficient Trust creation, as well as human onboarding for those who prefer a personal touch. Once you have selected your package, then whichever way you go, one of our wonderful Human Onboarding Specialists will complete the onboarding process with you and then schedule your kickoff meeting with your NY Estate Law .ai attorney. At the Kickoff meeting, our attorney will complete the information gathering and discuss your selected plan with you and your specific details, and will ensure that the plan you receive is tailored to your specific needs."],

    "GA122": ["How can the Estate Planning Template help you get started?",
    "The free Estate Planning Template helps you organize your personal information, list assets, and specify your wishes for executors, powers of attorney, and beneficiaries. You can then use this as a jumping off point to discuss your specific needs with your NY Estate Law .ai attorney."],

    "GA123": ["How does NY Estate Law .ai ensure customer satisfaction?",
    "NY Estate Law .ai guarantees customer satisfaction by offering clear pricing, professional legal guidance, and a refund option if your chosen package isn't the right fit after a consultation."],

    "GA124": ["What mistakes must I avoid in my estate plan?", 
    "When creating an estate plan, avoid common mistakes like failing to create or update the plan, overlooking digital assets, and neglecting long-term care. Make sure to name a guardian for minor children, choose a reliable executor or trustee, and plan for incapacity with a Power of Attorney and Health Care Proxy. Additionally, keep beneficiary designations up to date, consider tax implications, and avoid relying solely on a will—use a living trust to avoid probate and ensure privacy."],

    "GA125": ["How will my confidential information be protected?",
    "Your confidential information is kept strictly confidential and is not exposed to the internet or used in any AI training. As with any legal engagement, your confidential information may be disclosed to employees and contractors of NY Estate Law .ai, and with your permission, to other professionals such as accountants or financial planners, as necessary to fulfill your Estate Planning goals."],

    "GA126": ["User has intent to ask more questions?", "Great! Please feel free to ask."]

}

Retainer_QA_dict = {
   "RA1": ["What are the terms of the attorney-client relationship outlined in this agreement?",
            "The attorney-client relationship is strictly limited to legal services provided in connection with your Estate Planning goals. It does not cover any legal services outside of this scope."],
   "RA2": ["How will my confidential information be protected according to this agreement?",
            "Your confidential information may be disclosed to employees and contractors of NY Estate Law .ai, and with your permission, to other professionals such as accountants or financial planners, as necessary to fulfill your Estate Planning goals."],
   "RA5": ["How is the flat fee for legal services determined and negotiated?",
            "The flat fee is agreed upon between you and the firm and is considered fair and reasonable for the legal services provided. The exact amount is outlined in the agreement."],
   "RA7": ["Will I be informed about costs and expenses over $50 before they are incurred?",
            "Yes, you will be informed about any costs and expenses over $50 before they are incurred, and you will need to give verbal or written approval before they are approved."],
   "RA8": ["What happens if I do not approve a cost or expense that is necessary for my case?",
            "If you do not approve a necessary cost or expense, some aspect of your Estate Planning plan may not be able to move forward. The firm may advance such costs, but there is no obligation to do so, and you will need to reimburse them upon demand."],
   "RA10": ["What is the process for reimbursing any advances made on my behalf?",
            "You agree to reimburse the firm for any advances made on your behalf upon demand. This means the firm may pay costs upfront, but you will need to repay these advances when requested."],
   "RA11": ["How should I handle cancellations or delays for appointments with the firm?",
            "You should contact the office if you will be late or need to cancel an appointment. It is requested to give at least 24 hours' notice if you need to cancel an appointment."],
   "RA12": ["What is the procedure for booking an appointment to speak with an attorney?",
            "To book an appointment to speak with an attorney, you can use the booking link sent to you by email or you can contact the office directly. Support staff will help schedule your appointment according to availability."],
   "RA13": ["Who should I contact if I have legal questions outside of scheduled appointments?",
            "For legal questions outside of scheduled appointments, you should book an appointment to speak with one of the firm’s attorneys. Support staff can assist with scheduling."],
   "RA14": ["What should I do if I need to cancel an appointment with less than 24 hours’ notice?",
            "If you need to cancel an appointment with less than 24 hours' notice, you should contact the office as soon as possible."],
   "RA15": ["What services are included under this flat fee arrangement?",
            "The flat fee arrangement covers the legal services specified in connection with your Estate Planning goals, as detailed in the agreement. Any additional services or costs are not included in the flat fee."],
   "RA16": ["How will the firm communicate with me regarding any necessary disclosures of my information?",
            "The firm will use its judgment in making necessary disclosures of your information and will communicate with you accordingly. If other professionals are involved, you will be informed about any disclosures required for your best interests."],
   "RA17": ["Are there any additional fees or expenses that might arise during the course of representation?",
            "Yes, additional fees or expenses may arise, such as costs for filing fees, messenger services, or other necessary expenses. These will be communicated to you as they arise and must be approved before incurring them. It is also possible your needs may exceed the scope of the Standard Trust Packages offered, in which case, our attorney will advise you during your meeting."],
   "RA18": ["What steps are taken if additional professionals need to be involved in my case?",
            "If additional professionals need to be involved, the firm will disclose necessary information to them with your permission and use its judgment to ensure it benefits your Estate Planning goals."],
   "RA19": ["How does the firm determine whether a cost or expense is necessary?",
            "The firm uses its judgment to determine whether a cost or expense is necessary based on the requirements of your Estate Planning goals. Necessary costs will be communicated to you for approval."],
   "RA20": ["What is the firm's policy on client communication and appointments?",
            "The firm values timely communication and requests that you contact the office if you will be late or need to cancel an appointment. Appointments should be booked in advance, and any changes should be communicated as soon as possible."]
}

Objection_QA_dict = {
    "OA1": ["I’m not sure if an estate plan is really necessary for my situation or if my assets are valuable enough to justify one or I only have a few assets.",  
            "That's a common concern. The good news is that estate planning isn’t about the size of your assets but about ensuring your intentions are honored and your loved ones are cared for, no matter the value."],
    
    "OA2": ["I’m worried that the estate planning process will be too time-consuming or take too long.",  
            "I understand that. The good news is that we make the process as smooth and efficient as possible, so you can invest a little time now to ensure your loved ones are cared for and your legacy is secure."],
    
    "OA3": ["I’m concerned about the complexity of creating a trust or understanding the different types and their benefits.",  
            "That’s a reasonable concern. The good news is that while trusts might seem complex, we’ll simplify the process and tailor it to fit your needs, providing peace of mind and security for your family. We’ll also explain the different types of trusts in simple terms, helping you make informed decisions."],
    
    "OA4": ["What if I need to make changes to my estate plan in the future, or if my family’s needs or circumstances change?",  
            "I completely understand. The good news is that estate plans can and should adapt as your life evolves, ensuring your current wishes are always reflected and that any changes in your family’s needs are accounted for."],
    
    "OA5": ["I’m concerned about the impact of estate planning on my current financial situation or potential estate taxes.",  
            "That's a valid concern. The good news is that estate planning helps harmonize your current financial situation with long-term goals, and we develop strategies to minimize estate taxes, protecting your assets without adding stress."],
    
    "OA6": ["I don’t think I have enough knowledge to make informed decisions about my estate plan or all the decisions I need to make.",  
            "It’s completely understandable to feel that way. The good news is that we provide clear guidance every step of the way, empowering you to make informed decisions without feeling overwhelmed."],
    
    "OA7": ["I’m worried that my estate plan might not be legally binding or that it could be contested.",  
            "That’s a reasonable concern. The good news is that we ensure your estate plan meets all legal requirements, minimizing the chances of disputes by clearly documenting your intentions and ensuring they are respected."],
    
    "OA8": ["I don’t want to burden my family with the responsibility of managing my estate, or I’m concerned about potential family conflicts.",  
            "I understand your concern. The good news is that an estate plan can relieve your family of difficult decisions, providing clear guidance to manage your estate efficiently and preventing conflicts by clearly outlining your wishes."],
    
    "OA9": ["I’m worried about privacy and public records or the impact of estate planning on my privacy.",  
            "Privacy concerns are common. The good news is that we implement strategies like trusts to protect your personal information, keeping your estate matters private and secure."],
    
    "OA10": ["What if I don’t agree with the recommendations made by an estate planning attorney or don’t trust lawyers or legal documents?",  
             "I understand how you feel. The good news is that your estate plan should reflect your wishes. We work collaboratively, listening to your concerns to ensure the plan aligns with your vision, and we prioritize transparency, explaining every step to build trust."],
    
    "OA11": ["I’ve heard that estate planning is complicated, or I don’t know where to start with creating an estate plan.",  
             "It’s perfectly natural to feel uncertain. The good news is that we simplify the process, handling the complex details for you while guiding you step by step, identifying your needs and goals to create a customized plan."],
    
    "OA12": ["I’m unsure if my current plan is sufficient or if my estate plan is still valid with changing laws.",  
             "That’s a valid concern. The good news is that we’ll review your current plan and update it to reflect your evolving needs, and we offer regular reviews to keep your estate plan aligned with the latest laws, ensuring it remains effective."],
    
    "OA13": ["I’m worried about taxes and how they might impact my estate or the potential for estate taxes.",  
             "That’s understandable. The good news is that a well-structured plan can reduce taxes, ensuring more of your assets are preserved for your loved ones rather than going to taxes."],
    
    "OA14": ["I don’t want to give up control of my assets.",  
             "That’s a common concern. The good news is that with a revocable trust, you maintain full control of your assets while still enjoying the benefits of an estate plan."],
    
    "OA15": ["I’m too young to worry about an estate plan.",  
             "I hear you. The good news is that estate planning is not just for the elderly. It ensures your wishes are followed in case of emergencies, providing peace of mind regardless of your age."],
    
    "OA16": ["I already have a will, so I don’t need anything else.",  
             "That’s a good start. The good news is that a will is a great foundation, but a trust can offer more control, privacy, and flexibility in managing your assets and healthcare decisions."],
    
    "OA17": ["I don’t trust lawyers or legal documents.",  
             "That’s understandable. The good news is that we prioritize transparency, explaining every step to build trust and ensure you feel comfortable with the process and your decisions."],
    
    "OA18": ["I don’t have children, so I don’t need an estate plan.",  
             "That’s a valid concern. The good news is that estate planning helps ensure your assets are distributed to individuals or causes you care about, regardless of whether you have children."],
    
    "OA19": ["I don’t want to deal with the paperwork.",  
             "That’s understandable. The good news is that we handle most of the paperwork for you, walking you through the process step by step to make it as simple as possible."],
    
    "OA20": ["I’m not sure who to appoint as my executor or trustee.",  
             "That’s a common concern. The good news is that we can help you evaluate your options and even explore the possibility of appointing a professional fiduciary to ease your decision-making."],
    
    "OA21": ["I don’t want to make decisions about my medical care.",  
             "That’s a valid concern. The good news is that planning now ensures that your medical care wishes are clear, sparing your loved ones from making difficult decisions on your behalf."],
    
    "OA22": ["I’m concerned that my family might not understand or agree with my estate plan.",  
             "That’s a very real concern. The good news is that we help document your wishes clearly and can even assist in explaining your decisions to your family, fostering understanding and reducing disagreements."],
    
    "OA23": ["I’m worried about the cost of ongoing maintenance for my estate plan.",  
             "That’s understandable. The good news is that our estate plans are designed to minimize maintenance costs, ensuring long-term affordability while protecting your assets."],
    
    "OA24": ["I’m unsure if my estate plan is still valid with changing laws.",  
             "That’s a valid concern. The good news is that we offer regular reviews and updates to keep your estate plan aligned with the latest laws, ensuring it remains effective."],
    
    "OA25": ["I don’t have time to deal with it right now.",  
             "That’s a common worry. The good news is that we offer flexible scheduling to accommodate your availability, helping you create an estate plan without adding stress to your busy life."],
    
    "OA26": ["I don’t know where to start with creating an estate plan.",  
             "It’s perfectly normal to feel that way. The good news is that we guide you step by step, identifying your needs and goals to create a customized plan that fits your unique situation."],
    
    "OA27": ["I’m concerned about the potential for estate taxes.",  
             "That’s a valid concern. The good news is that we develop strategies to minimize estate taxes, protecting your assets and ensuring more of your wealth goes to your loved ones."],
    
    "OA28": ["I’ve heard estate planning is complicated.",  
             "That’s a common perception. The good news is that we simplify the process, handling the complex details for you while guiding you through each step with clarity."],
    
    "OA29": ["I don’t believe I need an estate plan because I trust my family.",  
             "That’s a valid point. The good news is that an estate plan complements your trust in your family by providing clear, legal documentation of your wishes, preventing future misunderstandings."],
    
    "OA30": ["I’m not wealthy, so I don’t need an estate plan.",  
             "I hear you. The good news is that an estate plan isn’t about wealth—it’s about control, ensuring your assets are managed according to your wishes, no matter their size."],
    
    "OA31": ["I’m worried about taxes and how they might impact my estate.",  
             "That’s a reasonable concern. The good news is that a well-structured plan can reduce taxes, ensuring more of your assets are preserved for your loved ones rather than going to taxes."],
    
    "OA32": ["I don’t want to give up control of my assets.",  
             "That’s understandable. The good news is that with a revocable trust, you maintain full control of your assets while still enjoying the benefits of an estate plan."],
    
    "OA33": ["I’m too young to worry about an estate plan.",  
             "I understand that feeling. The good news is that estate planning is not just for the elderly. It ensures your wishes are followed in case of emergencies, providing peace of mind regardless of your age."],
    
    "OA34": ["I don’t want to think about death.",  
             "That’s a sensitive issue for many. The good news is that estate planning isn’t just about death—it’s about ensuring your wishes are honored and your loved ones are protected, offering peace of mind while you're living."],
    
    "OA35": ["I already have a will, so I don’t need anything else.",  
             "That’s a good start. The good news is that while a will is important, a trust can offer more control, privacy, and flexibility in managing your assets and healthcare decisions."],
    
    "OA36": ["I don’t trust lawyers or legal documents.",  
             "That’s a concern many share. The good news is that we prioritize transparency, explaining every step to build trust and ensure you feel comfortable with the process and your decisions."],
    
    "OA37": ["I don’t have children, so I don’t need an estate plan.",  
             "That’s a valid concern. The good news is that estate planning helps ensure your assets are distributed to individuals or causes you care about, regardless of whether you have children."],
    
    "OA38": ["I don’t want to deal with the paperwork.",  
             "That’s understandable. The good news is that we handle most of the paperwork for you, walking you through the process step by step to make it as simple as possible."],
    
    "OA39": ["I’m not sure who to appoint as my executor or trustee.",  
             "That’s a common concern. The good news is that we can help you evaluate your options and even explore the possibility of appointing a professional fiduciary to ease your decision-making."],
    
    "OA40": ["I don’t want to make decisions about my medical care.",  
             "That’s a valid concern. The good news is that planning now ensures that your medical care wishes are clear, sparing your loved ones from making difficult decisions on your behalf."],
    
    "OA41": ["I’m worried about privacy and public records.",  
             "That’s a legitimate concern. The good news is that with a properly structured trust, your estate can bypass probate, keeping your personal information out of public records."],
    
    "OA42": ["I plan to give away my assets during my lifetime.",  
             "That’s a thoughtful plan. The good news is that an estate plan can complement your gifting strategy, ensuring everything is structured to avoid unnecessary taxes and complications."],
    
    "OA43": ["I don’t want to deal with potential family conflicts.",  
             "That’s a real concern for many. The good news is that a well-structured estate plan can prevent conflicts by clearly outlining your wishes and appointing a neutral third party to handle distributions."],
    
    "OA45": ["I’m worried about hidden fees or costs associated with estate planning.",  
             "That’s a valid concern. The good news is that we provide a clear breakdown of costs upfront and work within your budget, ensuring transparency and no unexpected financial surprises."]
}

General_QA_URL_Dict = {
    "GA1": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb7172d750aa738e3f.mp4',
    "GA2": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbb8d5541bb9dcc6fd.mp4',
    "GA3": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb48bae426b599776f.mp4',
    "GA4": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbb8d55416fddcc6fe.mp4',
    "GA5": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb6c2b349a7e55776b.mp4',
    "GA8": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb48bae410e999776c.mp4',
    "GA9": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb0fbb912aeb3ba899.mp4',
    "GA10": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb6c2b3454a755776c.mp4',
    "GA11": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbce7bbf1730c09beb.mp4',
    "GA13": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba6c2b34c9c8557769.mp4',
    "GA14": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb707cef59bb17910b.mp4',
    "GA15": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb6c2b3485b655776d.mp4',
    "GA16": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bab8d5544ae7dcc6fb.mp4',
    "GA17": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba0fbb91bbd83ba898.mp4',
    "GA18": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb48bae460df99776e.mp4',
    "GA19": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bac6a8397e24506985.mp4',
    "GA20": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba6c2b34ad30557768.mp4',
    "GA21": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba4e955631a7f26da8.mp4',
    "GA22": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbc7fd502b1dab4b06.mp4',
    "GA23": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbc7fd50734dab4b05.mp4',
    "GA26": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bace7bbfbb3bc09bea.mp4',
    "GA27": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbb8d5544e9ddcc6fc.mp4',
    "GA28": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba7172d7f8e3738e3e.mp4',
    "GA29": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bac6a8394a0f506984.mp4',
    "GA30": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb48bae4ce2799776d.mp4',
    "GA31": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba0fbb91f53d3ba896.mp4',
    "GA32": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba0fbb914dde3ba897.mp4',
    "GA33": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bac6a83951c8506988.mp4',
    "GA34": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba6c2b346efb55776a.mp4',
    "GA36": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba707cefe38317910a.mp4',
    "GA37": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba4e9556710ff26da7.mp4',
    "GA38": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba4e95562f19f26da9.mp4',
    "GA39": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bac6a83929e6506987.mp4',
    "GA40": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f05b31d5d0a8d108cd25ec.mp4',
    "GA41": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f05b31b32e47fa253ce832.mp4',
    "GA42": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f05b314b96a92364c4ff07.mp4',
    "GA44": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb0fbb91b1413ba89b.mp4',
    "GA45": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbc7fd5073faab4b07.mp4',
    "GA46": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bac6a839602d506983.mp4',
    "GA48": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bb0fbb9132203ba89a.mp4',
    "GA58": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64ba48bae4afc899776b.mp4',
    "GA59": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bab8d55446a3dcc6f9.mp4',
    "GA61": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbc7fd500dfbab4b08.mp4',
    "GA62": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbc6a839ca9a506989.mp4',
    "GA63": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bab8d5547c67dcc6fa.mp4',
    "GA64": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bac6a839681f506986.mp4',
    "GA65": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64bbc7fd5022d0ab4b04.mp4',
    "GA67": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896010a3a374db468b2.mp4',
    "GA68": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc28960c4f4e6a684cf2b7.mp4',
    "GA69": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e675e80f7014f25023f.mp4',
    "GA70": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896c6cc9b8f2b75bbfd.mp4',
    "GA71": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e675e80f77181250240.mp4',
    "GA73": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e67d5d0a84d81cd886e.mp4',
    "GA74": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896a94b9720a8729e46.mp4',
    "GA75": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e67b32e4744cd3d767d.mp4',
    "GA76": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e67d5d0a82753cd886c.mp4',
    "GA77": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e67d5d0a88f69cd886d.mp4',
    "GA78": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e67d4a305827d9a0c1b.mp4',
    "GA79": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e67988d2bcc8df0d53f.mp4',
    "GA80": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f07e675e80f72abe25023d.mp4',
    "GA81": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b988d2b0c71f0dee4.mp4',
    "GA82": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b5e80f73ec3251353.mp4',
    "GA83": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b5e80f705e5251352.mp4',
    "GA84": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896f7b0333c3cd7f5be.mp4',
    "GA85": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896ac6d17add057f705.mp4',
    "GA86": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd4a3056ef39a1c6d.mp4',
    "GA87": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b988d2b665ef0dee0.mp4',
    "GA88": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bb32e4731b23d7b8e.mp4',
    "GA89": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896725e69289473ce77.mp4',
    "GA90": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bb32e4746ad3d7b8d.mp4',
    "GA91": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896725e699b2b73ce76.mp4',
    "GA92": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd5d0a851d3cd90eb.mp4',
    "GA93": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd5d0a86025cd90ed.mp4',
    "GA94": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896e37d17548f03571b.mp4',
    "GA95": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b5e80f7621a251354.mp4',
    "GA96": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc28965bd0dbb619617386.mp4',
    "GA97": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd4a305cccb9a1c69.mp4',
    "GA98": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd5d0a85dd1cd90ec.mp4',
    "GA99": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b5e80f7b56f251356.mp4',
    "GA100": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd4a3059bb29a1c6a.mp4',
    "GA101": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc28965bd0dbb62d617385.mp4',
    "GA102": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879b5e80f74dac251357.mp4',
    "GA103": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896ac6d17f3b657f704.mp4',
    "GA104": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc289612c6594961d59dec.mp4',
    "GA105": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc289692b7b29c3b5ccbd9.mp4',
    "GA106": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66fc2896e8fa2458ad6af6c4.mp4',
    "GA108": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd4a305696e9a1c6e.mp4',
    "GA109": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd5d0a87c77cd90ee.mp4',
    "GA110": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0879bd5d0a8ff9dcd90ef.mp4',
    "GA111": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652aaed0c7fb3f099499.mp4',
    "GA112": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a1a36983bf3d214d6.mp4',
    "GA113": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a3c79963d4ac8cbcd.mp4',
    "GA114": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a85e87ffaf0816f15.mp4',
    "GA115": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652ac293c402323eb376.mp4',
    "GA116": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a744d7e27164344de.mp4',
    "GA117": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a96d490785a05c27f.mp4',
    "GA118": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a8f1ce6bd3b264f92.mp4',
    "GA119": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a8f1ce67884264f93.mp4',
    "GA120": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a3c79968474c8cbcc.mp4',
    "GA121": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652ab6e2b7b8fc14ef25.mp4',
    "GA122": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a96d4901a4505c27e.mp4',
    "GA123": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652ac293c4c0283eb377.mp4',
    "GA124": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a3c7996be3ec8cbcb.mp4',
    "GA125": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5652a85e87f9871816f16.mp4',
    "GA126": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5698433c0278101ce3385.mp4',
    # "GA127": '',
    # "GA128": '',
    # "GA129": '',
    # "GA130": '',
    # "GA131": '',
    # "GA132": '',
    # "GA133": '',
    # "GA134": '',
    # "GA135": '',
}

Objection_QA_URL_Dict = {
    "OA1": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c3a0249ce7d94d66c5.mp4',
    "OA2": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c298a215ca4c4678f6.mp4',
    "OA3": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c294aba1fc1823afa0.mp4',
    "OA4": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2ce539e809239bdf6.mp4',
    "OA5": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c32d95f3d0043067de.mp4',
    "OA6": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2f4e00637148822df.mp4',
    "OA7": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2403dfd482b9ede5e.mp4',
    "OA8": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2350bbe452a490204.mp4',
    "OA9": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2060cf627517ac653.mp4',
    "OA10": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2aeed8e4b618d8252.mp4',
    "OA11": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2ce539e844239bdf5.mp4',
    "OA12": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c3a7741e759fbbb3d5.mp4',
    "OA13": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c298a215e0714678f7.mp4',
    "OA14": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c294aba1614023af9f.mp4',
    "OA15": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c295d8750615c7144d.mp4',
    "OA16": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2850c6e381bac5f12.mp4',
    "OA17": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c295d8759a40c7144f.mp4',
    "OA18": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c298a215898c4678f5.mp4',
    "OA19": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2a0249c127d4d66c3.mp4',
    "OA20": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2f87f823e925f49a4.mp4',
    "OA21": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2403dfd2ee29ede5d.mp4',
    "OA22": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c272296725550066d6.mp4',
    "OA23": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c232bfcad01c4b474c.mp4',
    "OA24": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2722967d6ba0066d7.mp4',
    "OA25": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c232bfca18b54b474b.mp4',
    "OA26": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c232bfca28994b474a.mp4',
    "OA27": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c293c6514470f9c61a.mp4',
    "OA28": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2f4e00647968822e0.mp4',
    "OA29": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c27229675dce0066d5.mp4',
    "OA30": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2722967fcef0066d4.mp4',
    "OA31": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c3a7741e2b5ebbb3d3.mp4',
    "OA32": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c291ae0d0d14802c56.mp4',
    "OA33": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c295d8756d2dc7144e.mp4',
    "OA34": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2350bbe60b4490203.mp4',
    "OA35": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c294aba1de7523af9e.mp4',
    "OA36": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c291ae0d5820802c55.mp4',
    "OA37": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c298a21573a24678f4.mp4',
    "OA38": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c295d8755c1ac7144c.mp4',
    "OA39": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c293c6514ffdf9c618.mp4',
    "OA40": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c232bfcaeb0c4b4749.mp4',
    "OA41": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2722967bb150066d3.mp4',
    "OA42": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c23e3e103ba05206f9.mp4',
    "OA43": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c22d95f346113067dc.mp4',
    "OA45": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2850c6e5bf4ac5f11.mp4'
}

Retainer_QA_URL_Dict = {
   "RA1": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c294aba10eef23af9c.mp4',
   "RA2": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c293c65195c3f9c617.mp4',
   "RA5": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c294aba10a2723af9d.mp4',
   "RA7": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c22d95f361bb3067dd.mp4',
   "RA8": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2403dfd4d539ede5c.mp4',
   "RA10": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c294aba19dff23af9b.mp4',
   "RA11": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2a0249c17b44d66c2.mp4',
   "RA12": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2aeed8e6afc8d8251.mp4',
   "RA13": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2aeed8ecb7f8d8250.mp4',
   "RA14": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2f4e006df9f8822dd.mp4',
   "RA15": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2890f9220e51229d5.mp4',
   "RA16": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2060cf6e5b27ac652.mp4',
   "RA17": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c291ae0d0377802c54.mp4',
   "RA18": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2f4e0069b638822dc.mp4',
   "RA19": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2722967dd010066d2.mp4',
   "RA20": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ed88c2f4e00658408822de.mp4',
   }

Flow_QA_dict = {
    "FA1" : ["hi!","Hi. It's a wonderful day here in AI land, I hope it's a wonderful day for your too."],
    "FA2" : ["how are you?","I'm well thanks (as well as an AI can be that is), thanks for asking."],
    #"FA3" : ["i would like to buy the revocable one.","Thank you for that information, string4. Please let me know if you would like to make your Living Trust Package purchase in one, two, or three payments."],
    "FA4" : ["Can you tell me my name?","As a trained AI, I am currently trained to refrain from repeating back a potential client's private information, however, you can rest assured that the information you entered when you initiating the AI has been safely captured and stored and will be available to our wonderful team of humans."],
    "FA5" : ["Can you tell me my previous question?","As a trained AI, I'm not currently trained to lookup prior questions, however, you can feel free to ask me again. Please let me know if you are ready to purchase one of our Living Trust Packages. Let me know, string4, if you have any additional questions."],
    "FA6" : ["Can i please talk with a real person?","\n            I understand that you would like to speak to a Human, string4. That's a valid concern. The good news is we have some great humans for you to speak to! \n            It has been my pleasure assisting you. Please call 888-992-7979 and give them reference number 101, and our Human Onboarding \n            Specialists will extend to you our special 30% AI pricing discount as a courtesy for trying out our AI system. \n            Our goal is to make this a great experience for you, and I sincerely hope I have done that! \n            If you have any further questions, please feel free to ask."],
    "FA7" : ["yes i have more questions","Super, please let me know your question."],
    "FA8" : ["no","No Problem, you can ask me more questions if you need clarification on something."],
    "FA9" : ["i am ready to make the purchase.","That’s great, string4! I’m excited that you’ve decided to make a purchase today!"],
    "FA10" : ["tell me anything","\n            I'm sorry string4, as an AI, I'm only trained on very specific tasks. That is not a request I recognize. I will log the request so that a human can review and see if we should add it to my training. So please accept my apologies for the time being. In the meantime, would you please try to express your request differently?"],
    "FA11" : ["hi!","Hi. It's a wonderful day here in AI land, I hope it's a wonderful day for your too."],
    "FA12" : ["how are you?","I'm well thanks (as well as an AI can be that is), thanks for asking."],
    "FA13" : ["Can you tell me my name?","As a trained AI, I am currently trained to refrain from repeating back a potential client's private information, however, you can rest assured that the information you entered when you initiating the AI has been safely captured and stored and will be available to our wonderful team of humans."],
    "FA14" : ["Can you tell me my previous question?","As a trained AI, I'm not currently trained to lookup prior questions, however, you can feel free to ask me again. Please let me know if you are ready to purchase one of our Living Trust Packages. Let me know, string4, if you have any additional questions."],
    "FA15" : ["Can i please talk with a real person?","\n            I understand that you would like to speak to a Human, string4. That's a valid concern. The good news is we have some great humans for you to speak to! \n            It has been my pleasure assisting you. Please call 888-992-7979 and give them reference number 101, and our Human Onboarding \n            Specialists will extend to you our special 30% AI pricing discount as a courtesy for trying out our AI system. \n            Our goal is to make this a great experience for you, and I sincerely hope I have done that! \n            If you have any further questions, please feel free to ask."],
    "FA16" : ["yes i have more questions","Super, please let me know your question."],
    "FA17" : ["no","No Problem, you can ask me more questions if you need clarification on something."],
    "FA18" : ["tell me anything","\n            I'm sorry string4, as an AI, I'm only trained on very specific tasks. That is not a request I recognize. I will log the request so that a human can review and see if we should add it to my training. So please accept my apologies for the time being. In the meantime, would you please try to express your request differently?"],
    "FA19" : ["i would like to go with revocable trust package","Thank you for that information, string4. Please let me know if you would like to make your Living Trust Package purchase in one, two, or three payments. Let me know, string4, if you have any additional questions."],
    "FA20" : ["i want 7 payments","My apologies, but I am only programmed to approve a request of up to six monthly payments. Kindly choose between 1 and 6 payments. If you need a longer payment plan, please request to be transferred to a human, where you can discuss this with one of our wonderful Human Onboarding Specialists. Please let me know if you would like to make your Living Trust Package purchase in one, two, or three payments."],
    "FA21" : ["can you make 3 payments","\n            Thank you for that information, string4. I am now going to send you a link to your retainer agreement by email and text. \n            Also, I have some good news, string4. If you purchase your NY Estate Law .ai Living Trust Package in the next 15 minutes, \n            I’m authorized to give you an additional 10% off as a thank you for being an early adopter of our AI technology.\"\n     Please let me know when you have displayed your Retainer Agreement for your review. Let me know, string4, if you have any additional questions."],
    "FA22" : ["I am having an issue","I'm sorry you're having trouble, I will attempt to repeat my last task. If you continue to experience issues, please call 888-992-7979 to speak with one of our wonderful human Onboarding Specialists who will be able to assist you further. Please let me know when you have displayed your Retainer Agreement for your review. Let me know, string4, if you have any additional questions."],
    "FA23" : ["can you please change my package to irrevoacble","Not a problem. Please let me know when you have displayed your Retainer Agreement for your review. Let me know, string4, if you have any additional questions."],
    "FA24" : ["can you please change my payments to 5 as well","No problem. Please let me know when you have displayed your Retainer Agreement for your review."],
    "FA25" : ["how can i change my email?","\n        Certainly. I am not currently programmed to take updated information.\n        However, there are two ways to do that. You can continue with the current info and then tell your Onboarding Specialist of the change you would like to make.\n        Or, on the web pages, you can go to Step 3 and edit your info and put correct info in and save. Please note that if you change your email or phone number, this will restart the purchase process.\n     Please let me know when you have displayed your Retainer Agreement for your review. Let me know, string4, if you have any additional questions."],
    "FA26" : ["yes","Perfect! Once you have signed and made your payment, we'll get you booked with a Human Onboarding Specialist. Please let me know when you have signed your Retainer Agreement. Let me know, string4, if you have any additional questions."],
    "FA27" : ["I have signed the agreement","Excellent! I have sent you an Email with invoice link, Once you have made your payment, we'll get your onboarding appointment booked. Please let me know when you have made your payment. Let me know, string4, if you have any additional questions."],
    "FA28" : ["it's paid","\n           Thank you, string4, for placing your trust in NY Estate Law .ai. \n            You’ve now begun your Estate Planning journey and are on your way to achieving peace of mind! \n            \n\nNow it’s time to schedule your appointment with one of our Human Onboarding Specialists. \n            Your Human Onboarding appointment should only take 10-15 minutes. \n            I am sending you the Calendar Booking link by email and text. When you receive the link, please click it and select a date and time that is convenient for you. \n        Please let me know when you have booked your Onboarding meeting. Let me know, string4, if you have any additional questions."],
    "FA29" : ["yes","Awesome. You're going to love meeting your NY Estate Law .ai attorney and I know they are looking forward to meeting you. Please gather all your unique questions together and get ready for an incredible experience!Now that you've booked your Onboarding Specialist appointment, you and I are all wrapped up! My name is AI Kelley, and it has been my pleasure serving you. On behalf of everyone at NY Estate Law .ai, I want to thank you for your business. Our goal is to make this a great experience for you, and I sincerely hope I have done that! Let me know, string4, if you have any additional questions."]
}

# Iterate over both dictionaries and insert question-answer pairs along with their URLs
for key, value in General_QA_dict.items():
    General_QA_Collection.insert_one(
        {
            "GA": key,  # e.g., GA1, GA2
            "Question": value[0],  # the question part
            "Answer": value[1],  # the answer part
            "URL": General_QA_URL_Dict.get(key)  # fetch the corresponding URL from the URL dictionary
        }
    )


for key, value in Retainer_QA_dict.items():
    Retainer_QA_Collection.insert_one(
        {
            "GA": key,  # e.g., GA1, GA2
            "Question": value[0],  # the question part
            "Answer": value[1],  # the answer part
            "URL": Retainer_QA_URL_Dict.get(key)  # fetch the corresponding URL from the URL dictionary
        }
    )


for key, value in Objection_QA_dict.items():
    Objection_QA_Collection.insert_one(
        {
            "GA": key,  # e.g., GA1, GA2
            "Question": value[0],  # the question part
            "Answer": value[1],  # the answer part
            "URL": Objection_QA_URL_Dict.get(key)  # fetch the corresponding URL from the URL dictionary
        }
    )



