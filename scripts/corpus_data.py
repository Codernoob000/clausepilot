"""Curated Benchmark Corpus of 28 Market-Standard Freelance Clauses."""

CORPUS_CLAUSES = [
    # 1. Termination & Cancellation
    {
        "id": "std-term-01",
        "category": "Termination & Cancellation",
        "title": "Mutual 30-Day Notice for Convenience",
        "standard_text": "Either party may terminate this Agreement or any Statement of Work at any time without cause by giving at least thirty (30) days prior written notice to the other party.",
        "rationale": "Equal termination rights prevent unilateral lock-in and provide a predictable transition period for both freelancer cash flow and client onboarding.",
        "market_adoption_pct": 88,
        "unfavorable_signals": ["sole discretion", "immediate termination by client without notice", "contractor cannot terminate", "unilateral convenience termination"]
    },
    {
        "id": "std-term-02",
        "category": "Termination & Cancellation",
        "title": "Cause Termination with 10-Day Cure Period",
        "standard_text": "Either party may terminate this Agreement immediately upon written notice if the other party breaches any material term, provided the breaching party fails to cure such breach within ten (10) business days of receiving written notice specifying the breach.",
        "rationale": "A mandatory cure period prevents pretextual terminations and gives honest opportunities to rectify minor technical or operational disputes.",
        "market_adoption_pct": 91,
        "unfavorable_signals": ["no right to cure", "immediate termination without cause", "subjective dissatisfaction without notice"]
    },
    {
        "id": "std-term-03",
        "category": "Termination & Cancellation",
        "title": "Payment for Work-in-Progress Upon Termination",
        "standard_text": "In the event of termination for any reason, Client shall pay Contractor for all authorized Services performed, hours incurred, and non-cancelable expenses incurred up to the effective date of termination.",
        "rationale": "Guarantees that a contractor is compensated for actual labor and costs invested, regardless of whether a project is halted prematurely by the client.",
        "market_adoption_pct": 95,
        "unfavorable_signals": ["forfeiture of unpaid milestones", "no compensation upon cancellation", "refund of already completed work"]
    },
    {
        "id": "std-term-04",
        "category": "Termination & Cancellation",
        "title": "Kill Fee for Sudden Mid-Project Cancellation",
        "standard_text": "If Client cancels a scheduled sprint or project milestone with less than five (5) business days notice, Contractor shall be entitled to an early termination fee equal to 25% of the remaining milestone fee.",
        "rationale": "Compensates for calendar booking conflicts and lost alternative billable opportunities when work is abruptly cancelled.",
        "market_adoption_pct": 76,
        "unfavorable_signals": ["cancellation at any moment with zero fee", "no payment for reserved capacity"]
    },

    # 2. Payment Terms & Invoicing
    {
        "id": "std-pay-01",
        "category": "Payment Terms & Invoicing",
        "title": "Net-30 Payment Window",
        "standard_text": "Client agrees to pay all undisputed invoices within thirty (30) calendar days from the invoice issuance date.",
        "rationale": "Net-30 is the established standard across commercial service agreements, balancing client accounts payable cycles with freelancer working capital.",
        "market_adoption_pct": 82,
        "unfavorable_signals": ["Net-60", "Net-90", "paid when paid by end client", "conditional on end-customer approval"]
    },
    {
        "id": "std-pay-02",
        "category": "Payment Terms & Invoicing",
        "title": "Net-15 Accelerated Freelancer Terms",
        "standard_text": "Invoices for ongoing weekly or bi-weekly contractor services shall be due and payable within fifteen (15) calendar days of receipt.",
        "rationale": "Recognizes individual freelancers lack corporate credit lines and requires faster turnaround for recurring independent labor.",
        "market_adoption_pct": 68,
        "unfavorable_signals": ["Net-90 days", "quarterly payment cycle"]
    },
    {
        "id": "std-pay-03",
        "category": "Payment Terms & Invoicing",
        "title": "Late Payment Interest Fee",
        "standard_text": "Any undisputed amounts not paid when due shall accrue interest at the rate of 1.5% per month (or the maximum rate permitted by law, whichever is less) from the due date until paid in full.",
        "rationale": "Incentivizes timely payment and compensates contractor for administrative debt-collection overhead.",
        "market_adoption_pct": 79,
        "unfavorable_signals": ["no interest on late payments", "client may withhold payment indefinitely without penalty"]
    },
    {
        "id": "std-pay-04",
        "category": "Payment Terms & Invoicing",
        "title": "Right to Suspend Services for Past-Due Accounts",
        "standard_text": "If any undisputed invoice remains unpaid for more than fifteen (15) days past its due date, Contractor reserves the right to suspend performance of all Services until all outstanding balances are settled.",
        "rationale": "Protects contractors from compounding unrecoverable labor on delinquent client accounts.",
        "market_adoption_pct": 86,
        "unfavorable_signals": ["contractor must continue working without pay", "dispute delays all project fees"]
    },
    {
        "id": "std-pay-05",
        "category": "Payment Terms & Invoicing",
        "title": "10-Day Milestone Acceptance Window & Deemed Acceptance",
        "standard_text": "Client shall have ten (10) business days following deliverable submission to review and provide written notice of material non-conformity. In the absence of written feedback within said period, the deliverables shall be deemed accepted.",
        "rationale": "Prevents infinite review purgatory and establishes closure for deliverable sign-off and subsequent billing.",
        "market_adoption_pct": 84,
        "unfavorable_signals": ["unlimited review period", "discretionary sign-off without time limit", "deliverable rejected after indefinite delay"]
    },

    # 3. Intellectual Property & Work Product
    {
        "id": "std-ip-01",
        "category": "Intellectual Property & Work Product",
        "title": "IP Assignment Conditioned Upon Full Payment",
        "standard_text": "Upon Contractor's receipt of full and final payment for the applicable deliverables, Contractor hereby assigns to Client all right, title, and interest in and to the custom deliverables created under the SOW.",
        "rationale": "Ensures the contractor retains legal title as leverage until labor has actually been remunerated, preventing work theft.",
        "market_adoption_pct": 94,
        "unfavorable_signals": ["immediate assignment upon creation", "assignment irrespective of payment", "work-for-hire before payment clears"]
    },
    {
        "id": "std-ip-02",
        "category": "Intellectual Property & Work Product",
        "title": "Carve-Out of Pre-Existing IP & Reusable Tools",
        "standard_text": "Contractor retains full ownership of all pre-existing works, proprietary toolkits, code libraries, routines, and background IP owned or developed by Contractor prior to or independently of this Agreement. Contractor grants Client a perpetual, non-exclusive license to use such Background IP solely as embedded in the Deliverables.",
        "rationale": "Prevents client from claiming ownership over a freelancer's career-long assets, design templates, and reusable engineering libraries.",
        "market_adoption_pct": 92,
        "unfavorable_signals": ["assigns all prior inventions", "pre-existing IP transferred to client", "sole and exclusive ownership of all background code"]
    },
    {
        "id": "std-ip-03",
        "category": "Intellectual Property & Work Product",
        "title": "Portfolio & Case Study Showcase Rights",
        "standard_text": "Contractor shall retain the non-exclusive right to display non-confidential deliverables and describe project scope in Contractor's professional portfolio, case studies, and marketing materials.",
        "rationale": "Vital for freelance business growth; client confidentiality is preserved while permitting reasonable proof of craftsmanship.",
        "market_adoption_pct": 89,
        "unfavorable_signals": ["complete gag order on portfolio", "cannot mention client name or work", "perpetual secrecy on work samples"]
    },
    {
        "id": "std-ip-04",
        "category": "Intellectual Property & Work Product",
        "title": "Limited Commercial Moral Rights Waiver",
        "standard_text": "Contractor waives moral rights only to the extent necessary to permit Client to use, modify, and exploit the final custom deliverables for their intended commercial purpose.",
        "rationale": "Restricts moral rights waivers to specific project utility rather than broad, abusive personal degradation or false attribution.",
        "market_adoption_pct": 74,
        "unfavorable_signals": ["worldwide irrevocable moral rights waiver for all purposes", "contractor waives all reputation rights forever"]
    },
    {
        "id": "std-ip-05",
        "category": "Intellectual Property & Work Product",
        "title": "General Skill & Knowledge Retention",
        "standard_text": "Nothing in this Agreement shall prevent Contractor from using general ideas, concepts, algorithms, know-how, and techniques acquired or developed during the provision of the Services.",
        "rationale": "Protects contractor's professional knowledge base from being monopolized under broad IP claims.",
        "market_adoption_pct": 88,
        "unfavorable_signals": ["ownership of all concepts, ideas, and knowledge gained", "cannot reuse domain expertise"]
    },

    # 4. Non-Compete & Exclusivity
    {
        "id": "std-comp-01",
        "category": "Non-Compete & Exclusivity",
        "title": "Non-Exclusive Independent Contractor Status",
        "standard_text": "Contractor enters this Agreement as an independent contractor and retains the full right to perform services for other parties, provided such services do not breach Contractor's explicit confidentiality obligations.",
        "rationale": "Defines true independent contractor status under labor standards (e.g. IRS / ABC test); exclusivity risks worker misclassification.",
        "market_adoption_pct": 96,
        "unfavorable_signals": ["exclusive dedication of time", "cannot take other clients", "client approval required for outside work"]
    },
    {
        "id": "std-comp-02",
        "category": "Non-Compete & Exclusivity",
        "title": "No Post-Termination Industry Non-Compete",
        "standard_text": "Contractor shall not be subject to any post-termination restriction on providing services to any company or operating within any industry, market segment, or geographic area.",
        "rationale": "Post-contract non-competes on independent contractors are unenforceable in major jurisdictions (California, FTC rule) and severely impair livelihood.",
        "market_adoption_pct": 93,
        "unfavorable_signals": ["cannot work for competitors for 12 months", "global non-compete", "barred from industry post termination"]
    },
    {
        "id": "std-comp-03",
        "category": "Non-Compete & Exclusivity",
        "title": "Narrow Client & Staff Non-Solicitation",
        "standard_text": "During the term and for six (6) months thereafter, neither party shall actively solicit for employment the direct employees or primary subcontractors of the other party who were directly involved in the SOW.",
        "rationale": "Protects business stability without suffocating general market hiring or broad independent solicitation.",
        "market_adoption_pct": 81,
        "unfavorable_signals": ["2-year non-solicitation", "cannot work with any past, present, or prospective client of client"]
    },

    # 5. Limitation of Liability & Damages
    {
        "id": "std-liab-01",
        "category": "Limitation of Liability & Damages",
        "title": "Liability Capped at Total Fees Paid",
        "standard_text": "To the maximum extent permitted by applicable law, each party's aggregate liability under this Agreement shall be limited to the total fees paid or payable by Client to Contractor under the applicable Statement of Work during the preceding twelve (12) months.",
        "rationale": "Prevents catastrophic unbounded risk exposure disproportionate to the economic value of the consulting contract.",
        "market_adoption_pct": 89,
        "unfavorable_signals": ["unlimited contractor liability", "liability capped at 10x fees", "unilateral client liability cap only"]
    },
    {
        "id": "std-liab-02",
        "category": "Limitation of Liability & Damages",
        "title": "Mutual Exclusion of Consequential & Indirect Damages",
        "standard_text": "In no event shall either party be liable to the other for any indirect, incidental, consequential, special, punitive, or loss-of-profit damages arising out of or related to this Agreement.",
        "rationale": "Standard commercial protection against speculative or downstream revenue claims.",
        "market_adoption_pct": 92,
        "unfavorable_signals": ["contractor liable for lost profits", "client disclaims lost profits but contractor does not"]
    },
    {
        "id": "std-liab-03",
        "category": "Limitation of Liability & Damages",
        "title": "Exclusion of Personal Liability",
        "standard_text": "No officer, director, shareholder, employee, or individual representative of Contractor shall have any personal liability arising from this Agreement.",
        "rationale": "Protects individual freelancers and small LLC owners from personal asset jeopardy.",
        "market_adoption_pct": 90,
        "unfavorable_signals": ["personal guarantee required", "individual joint and several liability"]
    },
    {
        "id": "std-liab-04",
        "category": "Limitation of Liability & Damages",
        "title": "One-Year Statute of Limitations on Claims",
        "standard_text": "Any claim or action arising out of or relating to this Agreement must be commenced within one (1) year after the cause of action accrues, after which such claim shall be deemed barred.",
        "rationale": "Provides closure and avoids lingering legal liabilities years after project completion.",
        "market_adoption_pct": 78,
        "unfavorable_signals": ["indefinite claim window", "claims may be filed within 5 years"]
    },

    # 6. Indemnification & Warranties
    {
        "id": "std-ind-01",
        "category": "Indemnification & Warranties",
        "title": "Indemnification Limited to Willful IP Infringement",
        "standard_text": "Contractor shall indemnify and hold harmless Client against final third-party damage awards resulting directly from Contractor's willful infringement of a third party's registered copyright or trade secret in custom Deliverables created solely by Contractor.",
        "rationale": "Ties contractor indemnification strictly to their direct, fault-based intellectual output rather than unvetted third-party patents.",
        "market_adoption_pct": 83,
        "unfavorable_signals": ["indemnify against all third-party claims regardless of fault", "broad patent infringement indemnity"]
    },
    {
        "id": "std-ind-02",
        "category": "Indemnification & Warranties",
        "title": "Mutual Indemnification for Gross Negligence",
        "standard_text": "Each party shall indemnify, defend, and hold harmless the other party against direct damages arising from the indemnifying party's gross negligence, willful misconduct, or violation of applicable law.",
        "rationale": "Fairly balances severe fault scenarios across both sides without dumping asymmetrical risk onto the contractor.",
        "market_adoption_pct": 87,
        "unfavorable_signals": ["unilateral contractor indemnification", "client provides zero indemnity"]
    },
    {
        "id": "std-ind-03",
        "category": "Indemnification & Warranties",
        "title": "Carve-Out for Client-Supplied Assets & Unauthorized Edits",
        "standard_text": "Contractor shall have no obligation to indemnify Client for claims arising from materials, specifications, or assets provided by Client, or modifications made to Deliverables by any party other than Contractor.",
        "rationale": "Prevents freelancer from being held liable for copyright infringement or bugs introduced by client assets or client third-party edits.",
        "market_adoption_pct": 91,
        "unfavorable_signals": ["contractor indemnifies client even for client assets", "responsible for client alterations"]
    },

    # 7. Dispute Resolution & Governing Law
    {
        "id": "std-disp-01",
        "category": "Dispute Resolution & Governing Law",
        "title": "30-Day Mandatory Good-Faith Negotiation",
        "standard_text": "Prior to initiating formal arbitration or litigation, the parties agree to engage in good-faith informal negotiations for thirty (30) days to resolve any dispute arising under this Agreement.",
        "rationale": "De-escalates minor misunderstandings and avoids costly premature legal expenses.",
        "market_adoption_pct": 85,
        "unfavorable_signals": ["immediate lawsuit permitted", "unilateral court injunction without discussion"]
    },
    {
        "id": "std-disp-02",
        "category": "Dispute Resolution & Governing Law",
        "title": "Binding Neutral Arbitration or Small Claims Option",
        "standard_text": "Any dispute not resolved informally may be submitted to binding arbitration under the streamlined rules of the American Arbitration Association (AAA), or resolved in small claims court having jurisdiction.",
        "rationale": "Preserves a low-cost, accessible small claims path for unpaid freelancer invoices without forced enterprise arbitration fees.",
        "market_adoption_pct": 79,
        "unfavorable_signals": ["exclusive complex federal litigation", "mandatory arbitration with prohibitive administrative fees"]
    },
    {
        "id": "std-disp-03",
        "category": "Dispute Resolution & Governing Law",
        "title": "Home or Mutual Jurisdiction",
        "standard_text": "This Agreement shall be governed by the laws of the jurisdiction where Contractor resides or maintains their principal place of business, or by mutual virtual venue.",
        "rationale": "Prevents forcing an individual freelancer to travel across the country or overseas to defend an invoice claim.",
        "market_adoption_pct": 72,
        "unfavorable_signals": ["foreign offshore jurisdiction", "exclusive venue in client home state thousands of miles away"]
    },
    {
        "id": "std-disp-04",
        "category": "Dispute Resolution & Governing Law",
        "title": "Prevailing Party Legal Fee Recovery",
        "standard_text": "In any dispute or legal proceeding to enforce the terms of this Agreement or collect unpaid fees, the prevailing party shall be entitled to recover reasonable attorney fees and court costs.",
        "rationale": "Makes it viable for a freelancer to enforce smaller unpaid contract balances against a non-paying corporate client.",
        "market_adoption_pct": 84,
        "unfavorable_signals": ["contractor pays client legal fees regardless of outcome", "no fee recovery for contractor"]
    }
]
