"""
Synthetic University Academic Regulations Rulebook.

Each rule carries stable metadata: rule_id, chapter, section, subsection, title,
exact_text. The corpus deliberately contains ~20 MEANINGFUL, subtle contradictions
(see CONTRADICTIONS below) so the intelligence system can be demonstrated detecting
ANSWERABLE / NOT_ANSWERABLE / CONTRADICTORY situations. This module is the single
source of truth for the retrieval and reasoning layers.
"""

CHAPTERS = [
    {"code": "REG", "number": 1, "title": "Registration"},
    {"code": "ELI", "number": 2, "title": "Academic Eligibility"},
    {"code": "ATT", "number": 3, "title": "Attendance"},
    {"code": "EXM", "number": 4, "title": "Examinations"},
    {"code": "GRD", "number": 5, "title": "Grading"},
    {"code": "REX", "number": 6, "title": "Re-examinations and Supplementary Examinations"},
    {"code": "ASG", "number": 7, "title": "Assignments"},
    {"code": "PRJ", "number": 8, "title": "Project Requirements"},
    {"code": "INT", "number": 9, "title": "Internships"},
    {"code": "SCH", "number": 10, "title": "Scholarships"},
    {"code": "LEV", "number": 11, "title": "Leave"},
    {"code": "MIS", "number": 12, "title": "Academic Misconduct"},
    {"code": "DIS", "number": 13, "title": "Disciplinary Rules"},
    {"code": "APL", "number": 14, "title": "Appeals"},
    {"code": "GRAD", "number": 15, "title": "Graduation"},
    {"code": "DDL", "number": 16, "title": "Deadlines"},
    {"code": "EXC", "number": 17, "title": "Exceptions"},
    {"code": "ADM", "number": 18, "title": "Administrative Procedures"},
]

RULES = [
    # ------------------------------------------------------------------ REG
    {
        "rule_id": "REG-001", "chapter": "Registration", "section": "1.1 General Enrollment",
        "subsection": "Advisor Approval", "title": "Course registration approval",
        "exact_text": "Every student must register for their courses each semester through the online Student Portal. Registration is not considered complete until the student's assigned faculty advisor has reviewed and electronically approved the proposed course plan. Courses added without advisor approval carry no academic credit, and any grade earned in an unapproved course will not be recorded on the official transcript. Students bear sole responsibility for confirming that their registration status shows 'Approved' before classes begin.",
    },
    {
        "rule_id": "REG-002", "chapter": "Registration", "section": "1.1 General Enrollment",
        "subsection": "Registration Window", "title": "Registration window duration",
        "exact_text": "Registration for a semester opens on the first working day of the term. Students shall complete all course registration within the first two weeks of the semester. A student who fails to register within this two-week window is treated as not enrolled for that semester and forfeits attendance credit accrued before completion of registration.",
    },
    {
        "rule_id": "REG-005", "chapter": "Registration", "section": "1.2 Course Load",
        "subsection": "Maximum Credits", "title": "Maximum course load per semester",
        "exact_text": "The normal full-time course load is between 18 and 22 credits per semester. A student may register for a maximum of 24 credits in any single semester. Requests to register beyond the normal load must be justified by the student's cumulative academic performance and are reviewed by the advisor at the time of registration approval.",
    },
    {
        "rule_id": "REG-009", "chapter": "Registration", "section": "1.2 Course Load",
        "subsection": "Overload Permission", "title": "Credit overload for high performers",
        "exact_text": "Students in good academic standing may apply for a credit overload. Upon approval, the maximum permissible course load in a single semester is 27 credits. Overload applications are submitted to the Department Chair and must be accompanied by the student's most recent grade report. An overload once granted applies only to the semester for which it was requested.",
    },
    {
        "rule_id": "REG-012", "chapter": "Registration", "section": "1.3 Add and Drop",
        "subsection": "Course Drop", "title": "Dropping a course without penalty",
        "exact_text": "A student may drop a registered course without academic penalty and without a notation on the transcript up to the end of the third week of the semester. Courses dropped after this period but before the withdrawal deadline are recorded with a 'W' notation. A dropped course does not count toward the semester course load for the purpose of tuition assessment.",
    },

    # ------------------------------------------------------------------ ELI
    {
        "rule_id": "ELI-001", "chapter": "Academic Eligibility", "section": "2.1 Standing",
        "subsection": "Good Standing", "title": "Definition of good academic standing",
        "exact_text": "A student is in good academic standing when their cumulative grade point average (CGPA) is at or above 6.0 on the 10-point scale and they carry no more than one outstanding backlog course. Good academic standing is a precondition for holding elected student office, representing the university in external competitions, and applying for merit-based financial support.",
    },
    {
        "rule_id": "ELI-004", "chapter": "Academic Eligibility", "section": "2.2 Probation",
        "subsection": "Probation Trigger", "title": "Academic probation threshold",
        "exact_text": "A student whose cumulative grade point average falls below 5.0 at the end of any semester is placed on academic probation for the following semester. A student on academic probation may register for a reduced course load only and must meet fortnightly with their faculty advisor. Probation is lifted once the student's CGPA returns to 5.0 or above.",
    },
    {
        "rule_id": "ELI-007", "chapter": "Academic Eligibility", "section": "2.3 Honors Track",
        "subsection": "Entry Requirement", "title": "Eligibility for the honors track",
        "exact_text": "Admission to the honors track requires a cumulative grade point average of at least 8.0 maintained over two consecutive semesters, completion of at least 60 credits, and a recommendation from a faculty mentor. Honors students must complete an additional research thesis and are permitted to substitute one elective with an approved independent study.",
    },
    {
        "rule_id": "ELI-010", "chapter": "Academic Eligibility", "section": "2.4 Backlogs",
        "subsection": "Progression", "title": "Backlog limit for year progression",
        "exact_text": "A student may progress to the next academic year while carrying backlog courses, provided the number of uncleared courses does not exceed four at the time of progression. A student with five or more uncleared courses is required to repeat the year and re-register for the failed courses before enrolling in higher-year courses.",
    },

    # ------------------------------------------------------------------ ATT
    {
        "rule_id": "ATT-002", "chapter": "Attendance", "section": "3.1 Minimum Attendance",
        "subsection": "General Requirement", "title": "Minimum attendance to sit examinations",
        "exact_text": "A student must maintain a minimum of 75% attendance in each registered course, calculated across all scheduled lectures, tutorials, and laboratory sessions. A student who fails to meet the 75% attendance requirement in a course is barred from appearing in the end-semester examination for that course and is awarded a grade of 'F' (detained) unless a condonation is granted.",
    },
    {
        "rule_id": "ATT-005", "chapter": "Attendance", "section": "3.2 Special Categories",
        "subsection": "Honors Attendance", "title": "Attendance requirement for honors students",
        "exact_text": "Students enrolled on the honors track must maintain a minimum attendance of 85% in every course. Honors attendance is assessed at the end of each semester, and an honors student who drops below this threshold in two or more courses is reverted to the standard programme for the remainder of the degree.",
    },
    {
        "rule_id": "ATT-008", "chapter": "Attendance", "section": "3.3 Condonation",
        "subsection": "Medical Condonation", "title": "Condonation of shortfall in attendance",
        "exact_text": "A shortfall in attendance of up to 10 percentage points may be condoned once per semester where the student produces a valid medical certificate or documentation of an approved leave. Condonation is granted at the discretion of the Head of Department and requires the student to have attended at least 65% of sessions. Condonation does not apply to laboratory or clinical courses.",
    },

    # ------------------------------------------------------------------ EXM
    {
        "rule_id": "EXM-002", "chapter": "Examinations", "section": "4.1 Conduct",
        "subsection": "Hall Entry", "title": "Examination hall entry cut-off",
        "exact_text": "Candidates must be seated in the examination hall ten minutes before the scheduled start time. No candidate will be permitted to enter the examination hall after 30 minutes have elapsed from the start of the paper. No candidate will be permitted to leave the hall during the first 45 minutes or the final 15 minutes of the examination.",
    },
    {
        "rule_id": "EXM-003", "chapter": "Examinations", "section": "4.2 Exam Eligibility",
        "subsection": "Attendance Condition", "title": "Attendance condition to be eligible for exams",
        "exact_text": "To be eligible to appear in the end-semester examination for a course, a student must have attained at least 80% attendance in that course. The examination controller shall publish, one week before the examinations, a list of students detained on attendance grounds. A detained student may not sit the examination irrespective of internal assessment marks obtained.",
    },
    {
        "rule_id": "EXM-005", "chapter": "Examinations", "section": "4.3 Re-evaluation",
        "subsection": "Re-evaluation Window", "title": "Request window for answer-script re-evaluation",
        "exact_text": "A student who wishes to have an end-semester answer script re-evaluated must submit a re-evaluation request, with the prescribed fee, within 15 days of the declaration of results. Re-evaluation is limited to verification of totalling and re-marking against the official scheme. The revised marks, whether higher or lower, replace the original marks on the transcript.",
    },
    {
        "rule_id": "EXM-008", "chapter": "Examinations", "section": "4.4 Grace Provisions",
        "subsection": "Grace Marks", "title": "Grace marks to clear a course",
        "exact_text": "Where a student fails a single course by a narrow margin, the examination board may award up to 3 grace marks in that course to enable the student to reach the passing threshold. Grace marks may be applied to at most one course per semester and are shown separately on the internal record but not on the transcript.",
    },
    {
        "rule_id": "EXM-011", "chapter": "Examinations", "section": "4.5 Malpractice",
        "subsection": "Exam Malpractice", "title": "Consequence of examination malpractice",
        "exact_text": "Any candidate found using unfair means during an examination, including unauthorised materials or electronic devices, shall have that examination cancelled and be reported to the Disciplinary Committee. A first instance of examination malpractice results in cancellation of the paper concerned; the committee may impose further penalties under the disciplinary rules.",
    },

    # ------------------------------------------------------------------ GRD
    {
        "rule_id": "GRD-001", "chapter": "Grading", "section": "5.1 Grade Scale",
        "subsection": "Letter Grades", "title": "Letter grade to grade-point mapping",
        "exact_text": "The university uses a 10-point grading scale. Letter grades map to grade points as follows: O (outstanding) = 10, A = 9, B = 8, C = 7, D = 6, E = 5, and F (fail) = 0. The grade point average is computed as the credit-weighted mean of grade points across all registered courses in the assessment period.",
    },
    {
        "rule_id": "GRD-003", "chapter": "Grading", "section": "5.2 Passing",
        "subsection": "Passing Grade", "title": "Minimum passing grade in a course",
        "exact_text": "The minimum passing grade in any course is 'D', corresponding to a course score of 40%. A student who earns a grade of 'E' or below is deemed to have failed the course and must re-register for or re-attempt it. A pass grade, once earned, cannot be improved by re-registering except under the grade-improvement provisions.",
    },
    {
        "rule_id": "GRD-008", "chapter": "Grading", "section": "5.3 Progression Grades",
        "subsection": "Core Course Passing", "title": "Passing standard for core courses",
        "exact_text": "For all core (non-elective) courses, a student must obtain a minimum grade of 'C', equivalent to a score of 50%, to be considered to have passed the course. A grade below 'C' in a core course, even if numerically above the general pass mark, requires the student to re-attempt the course at the next available offering.",
    },
    {
        "rule_id": "GRD-010", "chapter": "Grading", "section": "5.4 No Grace",
        "subsection": "Grace Prohibition", "title": "Prohibition on grace marks",
        "exact_text": "Grades are awarded strictly on the marks obtained in internal assessment and the end-semester examination. No grace marks, moderation uplift, or discretionary adjustment of any kind shall be applied to raise a failing score to a passing grade. Marks recorded by the examiner are final subject only to the formal re-evaluation process.",
    },
    {
        "rule_id": "GRD-013", "chapter": "Grading", "section": "5.5 Improvement",
        "subsection": "Grade Improvement", "title": "Grade improvement attempts",
        "exact_text": "A student who has passed a course may attempt to improve the grade by re-registering for the end-semester examination once. The better of the two grades is retained on the transcript. Grade improvement is not available for courses in which the student was penalised for academic misconduct, and it may not be used to alter internal assessment marks.",
    },

    # ------------------------------------------------------------------ REX
    {
        "rule_id": "REX-001", "chapter": "Re-examinations and Supplementary Examinations",
        "section": "6.1 Eligibility", "subsection": "Who May Apply",
        "title": "Eligibility for supplementary examinations",
        "exact_text": "A student who fails a course, or who was absent from an end-semester examination with valid cause, is eligible to appear in the supplementary examination held before the start of the following semester. The internal assessment marks earned during the regular semester are carried forward and combined with the supplementary examination marks to determine the final grade.",
    },
    {
        "rule_id": "REX-002", "chapter": "Re-examinations and Supplementary Examinations",
        "section": "6.2 Attempts", "subsection": "Attempt Limit",
        "title": "Number of supplementary attempts per course",
        "exact_text": "A student may attempt the supplementary examination for a failed course a maximum of two times. If the student has not cleared the course after two supplementary attempts, the course must be repeated in full, including re-attending classes and re-earning the internal assessment marks, at the next regular offering.",
    },
    {
        "rule_id": "REX-006", "chapter": "Re-examinations and Supplementary Examinations",
        "section": "6.3 Repeat Policy", "subsection": "Single Attempt Rule",
        "title": "Supplementary attempt permitted per course",
        "exact_text": "Only one supplementary attempt is permitted per failed course. A student who does not pass the course in that single supplementary attempt is required to re-register for the course during a regular semester. This single-attempt rule ensures that supplementary examinations do not become a substitute for regular course engagement.",
    },
    {
        "rule_id": "REX-009", "chapter": "Re-examinations and Supplementary Examinations",
        "section": "6.4 Registration", "subsection": "Supplementary Fee",
        "title": "Supplementary examination registration fee",
        "exact_text": "Registration for a supplementary examination requires payment of the prescribed per-course fee at least 10 days before the scheduled supplementary examination date. Late registration is not accepted for supplementary examinations. A student who has registered but does not appear forfeits the fee and the attempt is counted as used.",
    },

    # ------------------------------------------------------------------ ASG
    {
        "rule_id": "ASG-001", "chapter": "Assignments", "section": "7.1 Weightage",
        "subsection": "Internal Weight", "title": "Weight of assignments in internal assessment",
        "exact_text": "Assignments contribute to the internal (continuous) assessment component of a course. Unless the course syllabus specifies otherwise, assignments collectively account for 20% of the internal assessment marks. The remaining internal marks derive from quizzes, mid-semester tests, and, where applicable, laboratory work.",
    },
    {
        "rule_id": "ASG-003", "chapter": "Assignments", "section": "7.2 Submission",
        "subsection": "Late Submission", "title": "Late submission of assignments",
        "exact_text": "Assignments submitted after the due date will be accepted up to 5 calendar days late, subject to a penalty of 10% of the assignment marks for each day of delay. Assignments submitted more than 5 days late are not graded and receive zero. This provision applies uniformly to individual and group assignments.",
    },
    {
        "rule_id": "ASG-006", "chapter": "Assignments", "section": "7.3 Integrity",
        "subsection": "Collaboration", "title": "Permitted collaboration on assignments",
        "exact_text": "Students may discuss assignment concepts with peers, but the submitted work must be composed individually unless the assignment is expressly designated as group work. Copying another student's solution, submitting purchased or shared solutions, or reusing a previous cohort's work constitutes academic misconduct and is dealt with under Chapter 12.",
    },

    # ------------------------------------------------------------------ PRJ
    {
        "rule_id": "PRJ-001", "chapter": "Project Requirements", "section": "8.1 Capstone",
        "subsection": "Requirement", "title": "Mandatory final-year capstone project",
        "exact_text": "Every undergraduate student must complete a final-year capstone project carrying 12 credits, spread across the two semesters of the final year. The project comprises a problem definition phase, an implementation phase, and a final defence before a panel of at least two faculty examiners. A passing grade in the capstone project is a prerequisite for graduation.",
    },
    {
        "rule_id": "PRJ-003", "chapter": "Project Requirements", "section": "8.2 Teams",
        "subsection": "Team Size", "title": "Maximum project team size",
        "exact_text": "Capstone projects may be undertaken individually or in teams. Where a team is formed, the maximum team size is 4 students. Every team member must contribute an identifiable and assessable portion of the work, and the final defence includes an individual viva to confirm each member's contribution.",
    },
    {
        "rule_id": "PRJ-006", "chapter": "Project Requirements", "section": "8.3 Group Norms",
        "subsection": "Group Composition", "title": "Team composition limit",
        "exact_text": "To ensure equitable workload distribution, a project group shall consist of no more than 3 students. Groups exceeding this composition will not be approved by the project coordinator, and the scope of each project is calibrated by the coordinator to the number of members so that assessment remains fair across teams of different sizes.",
    },
    {
        "rule_id": "PRJ-009", "chapter": "Project Requirements", "section": "8.4 Reports",
        "subsection": "Submission", "title": "Project report submission requirement",
        "exact_text": "The final project report must be submitted in the prescribed format no later than two weeks before the scheduled defence. The report must include an originality declaration signed by all team members and pass an automated similarity check with a similarity index below 15%. Reports failing the similarity check are returned for revision and may delay the defence.",
    },

    # ------------------------------------------------------------------ INT
    {
        "rule_id": "INT-002", "chapter": "Internships", "section": "9.1 Duration",
        "subsection": "Minimum Duration", "title": "Minimum internship duration",
        "exact_text": "The mandatory industry internship must be of a minimum duration of 8 weeks of full-time engagement, ordinarily undertaken during the summer break between the third and fourth years. The internship carries 4 credits and is assessed on the basis of an employer evaluation, a written report, and a presentation to the department.",
    },
    {
        "rule_id": "INT-003", "chapter": "Internships", "section": "9.2 Eligibility",
        "subsection": "Credit Prerequisite", "title": "Credits required before internship",
        "exact_text": "A student becomes eligible to undertake the mandatory internship only after successfully completing at least 90 credits of coursework. Students who have not accumulated the required credits by the summer of the third year must defer the internship to a later approved period, in consultation with the internship coordinator.",
    },
    {
        "rule_id": "INT-006", "chapter": "Internships", "section": "9.3 Flexible Track",
        "subsection": "Duration Flexibility", "title": "Internship duration under flexible track",
        "exact_text": "For students pursuing the flexible study track, an internship of a minimum duration of 6 weeks is sufficient to earn the internship credits, provided the employer certifies full-time engagement and the report demonstrates the prescribed learning outcomes. The reduced duration reflects the more intensive project scope expected on the flexible track.",
    },
    {
        "rule_id": "INT-007", "chapter": "Internships", "section": "9.2 Eligibility",
        "subsection": "Credit Threshold", "title": "Credit threshold for internship registration",
        "exact_text": "Registration for the internship requires that a student has earned a minimum of 100 credits and cleared all first- and second-year backlogs. The internship coordinator verifies credit completion at the time of internship registration, and students falling short of the threshold are advised to complete pending courses before applying.",
    },

    # ------------------------------------------------------------------ SCH
    {
        "rule_id": "SCH-002", "chapter": "Scholarships", "section": "10.1 Merit Award",
        "subsection": "CGPA Requirement", "title": "Merit scholarship CGPA requirement",
        "exact_text": "The merit scholarship is awarded to students who maintain a cumulative grade point average of at least 8.0 and have no backlog courses. The award covers 50% of tuition for the subsequent semester and is renewed each semester subject to continued satisfaction of the eligibility criteria. A student penalised for misconduct forfeits the scholarship.",
    },
    {
        "rule_id": "SCH-005", "chapter": "Scholarships", "section": "10.2 Renewal",
        "subsection": "Renewal Threshold", "title": "Scholarship renewal CGPA threshold",
        "exact_text": "To retain a merit scholarship in subsequent semesters, a student must maintain a cumulative grade point average of at least 7.5. Where a student's CGPA falls below this renewal threshold, the scholarship is suspended for one semester; it may be reinstated if the student restores the required average in the following semester.",
    },
    {
        "rule_id": "SCH-003", "chapter": "Scholarships", "section": "10.3 Disbursement",
        "subsection": "Payment Timing", "title": "Scholarship disbursement timeline",
        "exact_text": "Approved scholarship amounts are disbursed to the student's registered account within 30 days of the publication of the semester results on which the award is based. Students must ensure their bank details on file are current; disbursement delayed due to incorrect details is not the responsibility of the finance office.",
    },
    {
        "rule_id": "SCH-008", "chapter": "Scholarships", "section": "10.4 Attendance Condition",
        "subsection": "Attendance for Merit", "title": "Attendance condition for merit awards",
        "exact_text": "In addition to academic performance, recipients of merit awards must maintain an attendance of at least 90% across all courses in the qualifying semester. Attendance below this level disqualifies the student from receiving the award for that period, regardless of the grade point average achieved.",
    },

    # ------------------------------------------------------------------ LEV
    {
        "rule_id": "LEV-001", "chapter": "Leave", "section": "11.1 Application",
        "subsection": "Procedure", "title": "Procedure for applying for leave",
        "exact_text": "A student who needs to be absent must apply for leave in advance through the Student Portal, stating the reason and the dates. Leave applications of more than three days must be supported by documentation and are approved by the Head of Department. Leave, once approved, is recorded but does not automatically restore attendance for the missed sessions unless condoned.",
    },
    {
        "rule_id": "LEV-002", "chapter": "Leave", "section": "11.2 Medical Leave",
        "subsection": "Medical Entitlement", "title": "Medical leave entitlement per semester",
        "exact_text": "A student may avail medical leave of up to 15 days in a semester, supported by a certificate from a registered medical practitioner. Days taken as approved medical leave are excluded from the attendance denominator for the affected courses, subject to submission of the certificate within seven days of returning to class.",
    },
    {
        "rule_id": "LEV-006", "chapter": "Leave", "section": "11.3 Leave Caps",
        "subsection": "Aggregate Medical Cap", "title": "Cap on medical leave",
        "exact_text": "Medical leave is capped at 10 days per semester. Any absence on medical grounds beyond this cap is treated as ordinary absence and counts against the student's attendance, even where a medical certificate is produced. Students with prolonged illness beyond the cap should instead apply for a semester break under the exceptions chapter.",
    },
    {
        "rule_id": "LEV-009", "chapter": "Leave", "section": "11.4 Duty Leave",
        "subsection": "Representation", "title": "Duty leave for university representation",
        "exact_text": "Students representing the university in officially sanctioned sports, cultural, or academic events are granted duty leave for the period of the event and reasonable travel. Duty leave is counted as attendance for all affected courses, provided the student submits the official participation certificate to the department within one week of the event.",
    },

    # ------------------------------------------------------------------ MIS
    {
        "rule_id": "MIS-001", "chapter": "Academic Misconduct", "section": "12.1 Definition",
        "subsection": "Scope", "title": "Definition of academic misconduct",
        "exact_text": "Academic misconduct includes plagiarism, unauthorised collaboration, fabrication or falsification of data, impersonation in examinations, and any attempt to gain an unfair academic advantage. All allegations of academic misconduct are documented and referred to the Academic Integrity Committee for inquiry, and the student is given an opportunity to respond before any penalty is imposed.",
    },
    {
        "rule_id": "MIS-002", "chapter": "Academic Misconduct", "section": "12.2 Plagiarism",
        "subsection": "First Offence", "title": "Penalty for first plagiarism offence",
        "exact_text": "For a first proven offence of plagiarism in an assignment, the penalty is a mark of zero on the assignment concerned. The student is issued a formal written warning that is placed on their record, and is required to attend a workshop on academic writing and citation. A first offence does not, by itself, affect the grade in other components of the course.",
    },
    {
        "rule_id": "MIS-005", "chapter": "Academic Misconduct", "section": "12.3 Consequences",
        "subsection": "First Instance Penalty", "title": "Consequence of a first misconduct instance",
        "exact_text": "A first instance of plagiarism results in the student failing the entire course in which the misconduct occurred, with a grade of 'F' recorded on the transcript. The Academic Integrity Committee may, in addition, bar the student from applying for scholarships for one academic year. Repeat instances lead to suspension.",
    },
    {
        "rule_id": "MIS-008", "chapter": "Academic Misconduct", "section": "12.4 Repeat Offences",
        "subsection": "Escalation", "title": "Penalty for repeated misconduct",
        "exact_text": "A second proven instance of academic misconduct of any kind results in the student failing all courses of the semester in which it occurred. A third instance results in a recommendation for expulsion, which is decided by the Disciplinary Committee. The student's right to appeal under Chapter 14 is preserved at every stage.",
    },

    # ------------------------------------------------------------------ DIS
    {
        "rule_id": "DIS-001", "chapter": "Disciplinary Rules", "section": "13.1 Conduct",
        "subsection": "Code", "title": "General code of conduct",
        "exact_text": "Students are expected to conduct themselves with integrity and respect on campus and at all university-affiliated activities. Behaviour that endangers others, damages property, disrupts teaching, or brings the university into disrepute constitutes a disciplinary offence. Disciplinary matters are handled by the Disciplinary Committee, which may impose warnings, fines, suspension, or expulsion depending on severity.",
    },
    {
        "rule_id": "DIS-004", "chapter": "Disciplinary Rules", "section": "13.2 Academic Discipline",
        "subsection": "Performance Probation", "title": "Disciplinary probation on performance",
        "exact_text": "A student whose cumulative grade point average falls below 4.5 is placed on disciplinary-academic probation and is required to sign an academic improvement contract. Failure to meet the terms of the improvement contract within one semester may result in the student being asked to withdraw from the programme.",
    },
    {
        "rule_id": "DIS-007", "chapter": "Disciplinary Rules", "section": "13.3 Suspension",
        "subsection": "Effect", "title": "Effect of suspension on academic record",
        "exact_text": "A student under suspension may not attend classes, sit examinations, use university facilities, or represent the university for the duration of the suspension. Time spent under suspension counts as absence, and examinations missed during suspension are not eligible for the supplementary route unless the appeal body directs otherwise.",
    },

    # ------------------------------------------------------------------ APL
    {
        "rule_id": "APL-001", "chapter": "Appeals", "section": "14.1 Right of Appeal",
        "subsection": "General", "title": "Right to appeal an academic decision",
        "exact_text": "A student has the right to appeal an academic or disciplinary decision that affects their standing. All appeals must be made in writing to the Office of Academic Affairs, stating the grounds of appeal and enclosing supporting evidence. An appeal does not suspend the operation of the decision unless the appeal body orders a stay.",
    },
    {
        "rule_id": "APL-002", "chapter": "Appeals", "section": "14.2 Time Limit",
        "subsection": "Filing Window", "title": "Time limit to file an appeal",
        "exact_text": "An appeal against a declared result or an academic penalty must be filed within 7 days of the date on which the result or decision was communicated to the student. Appeals received after this period are ordinarily time-barred, and the appeal body may decline to consider them except in demonstrable cases of hardship.",
    },
    {
        "rule_id": "APL-005", "chapter": "Appeals", "section": "14.3 Extended Window",
        "subsection": "Filing Deadline", "title": "Deadline for lodging an appeal",
        "exact_text": "A student wishing to contest a decision must lodge the appeal within 14 days of the communication of that decision. The 14-day period is intended to give students adequate time to gather supporting documentation. The appeal body meets at least once a month to dispose of pending appeals.",
    },
    {
        "rule_id": "APL-006", "chapter": "Appeals", "section": "14.4 Re-evaluation Appeals",
        "subsection": "Script Review Window", "title": "Window to seek re-evaluation of scripts",
        "exact_text": "A request for re-evaluation of an examination answer script, treated as an appeal on the assessment, must be submitted within 7 days of the publication of results. This window is separate from the general appeal timeline and applies specifically to disputes about the marking of examination scripts.",
    },

    # ------------------------------------------------------------------ GRAD
    {
        "rule_id": "GRAD-001", "chapter": "Graduation", "section": "15.1 Requirements",
        "subsection": "Overview", "title": "General graduation requirements",
        "exact_text": "To graduate, a student must clear all registered courses with at least the minimum passing grade, complete the mandatory internship and capstone project, have no outstanding disciplinary penalties, and clear all dues to the university. The degree is conferred at the annual convocation following certification by the Board of Examinations.",
    },
    {
        "rule_id": "GRAD-002", "chapter": "Graduation", "section": "15.2 Credits",
        "subsection": "Credit Requirement", "title": "Total credits required to graduate",
        "exact_text": "A student must accumulate a minimum of 160 credits to be eligible for the award of the undergraduate degree. These credits must include all designated core courses, the internship, and the capstone project. Excess credits earned through additional electives are recorded but do not reduce the core requirement.",
    },
    {
        "rule_id": "GRAD-007", "chapter": "Graduation", "section": "15.3 Credit Audit",
        "subsection": "Minimum Credits", "title": "Minimum credits for degree award",
        "exact_text": "The degree audit confirms that, to graduate, a student has earned the total number of credits required for the undergraduate degree, namely at least 156 credits across the programme, including all mandatory components. The audit is performed by the examinations office in the final semester, and any credit shortfall must be made good through approved courses before the degree can be conferred.",
    },
    {
        "rule_id": "GRAD-004", "chapter": "Graduation", "section": "15.4 Distinction",
        "subsection": "Award of Distinction", "title": "Award of degree with distinction",
        "exact_text": "A degree is awarded with distinction to a student who attains a final cumulative grade point average of 8.5 or above, has cleared every course on the first attempt with no supplementary examinations, and has no record of academic misconduct. Distinction is noted on the degree certificate and the final transcript.",
    },

    # ------------------------------------------------------------------ DDL
    {
        "rule_id": "DDL-002", "chapter": "Deadlines", "section": "16.1 Registration Deadlines",
        "subsection": "Course Registration", "title": "Deadline to complete course registration",
        "exact_text": "Course registration for a semester must be completed within the first 10 days of the term. The Student Portal closes registration automatically at the end of the tenth day, and any student who has not completed registration by then must apply for late registration with a penalty fee and departmental approval.",
    },
    {
        "rule_id": "DDL-004", "chapter": "Deadlines", "section": "16.2 Submission Deadlines",
        "subsection": "Assignment Cut-off", "title": "Assignment submission cut-off",
        "exact_text": "All assignments must be submitted on or before the due date and time published in the course plan. No assignment will be accepted after the deadline, and the submission portal closes automatically at the stated time. Students are advised to submit well ahead of the deadline to avoid loss of marks due to technical issues.",
    },
    {
        "rule_id": "DDL-006", "chapter": "Deadlines", "section": "16.3 Withdrawal Deadline",
        "subsection": "Course Withdrawal", "title": "Deadline to withdraw from a course",
        "exact_text": "A student may withdraw from a course, with a 'W' recorded on the transcript, up to the end of the eighth week of the semester. After the eighth week no withdrawal is permitted and the student receives the grade earned in the course. Withdrawal does not entitle the student to any tuition refund.",
    },
    {
        "rule_id": "DDL-009", "chapter": "Deadlines", "section": "16.4 Results",
        "subsection": "Result Declaration", "title": "Timeline for declaration of results",
        "exact_text": "End-semester results are declared within 30 days of the conclusion of the last examination of the session. Internal assessment marks are published to students before the end-semester examinations so that discrepancies may be raised and corrected in advance of the final result computation.",
    },

    # ------------------------------------------------------------------ EXC
    {
        "rule_id": "EXC-001", "chapter": "Exceptions", "section": "17.1 Semester Break",
        "subsection": "Approved Break", "title": "Approved semester break",
        "exact_text": "A student facing prolonged illness or exceptional personal circumstances may apply for an approved semester break of up to two semesters. During an approved break the student's registration is frozen and no tuition accrues. The student resumes at the point of interruption and the break does not count toward the maximum time allowed to complete the degree.",
    },
    {
        "rule_id": "EXC-003", "chapter": "Exceptions", "section": "17.2 Overload Exception",
        "subsection": "Discretionary Overload", "title": "Discretionary credit overload",
        "exact_text": "In exceptional cases, and to enable a final-year student to graduate on time, the Dean may permit a course load of up to 27 credits in a single semester notwithstanding the ordinary maximum. Such permission is granted in writing, is specific to the named semester, and requires the student to be clear of backlogs.",
    },
    {
        "rule_id": "EXC-004", "chapter": "Exceptions", "section": "17.3 Late Withdrawal",
        "subsection": "Withdrawal Extension", "title": "Extended withdrawal on hardship",
        "exact_text": "Where a student experiences documented hardship, withdrawal from a course may be permitted up to the end of the tenth week of the semester, extending the ordinary withdrawal window. Late withdrawal on hardship grounds is approved by the Dean of Students and is recorded with a 'W' notation without academic penalty.",
    },

    # ------------------------------------------------------------------ ADM
    {
        "rule_id": "ADM-001", "chapter": "Administrative Procedures", "section": "18.1 Records",
        "subsection": "Transcripts", "title": "Issue of official transcripts",
        "exact_text": "Official transcripts are issued by the examinations office on written request and payment of the prescribed fee. A standard transcript is prepared within five working days of a valid request. Transcripts are released only to the student or to a third party expressly authorised in writing by the student.",
    },
    {
        "rule_id": "ADM-004", "chapter": "Administrative Procedures", "section": "18.2 Finance",
        "subsection": "Scholarship Processing", "title": "Processing time for scholarship payments",
        "exact_text": "Once a scholarship is sanctioned, the finance office processes and releases the payment within 45 days of receiving the sanction order from the scholarships committee. Students may track the status of their payment through the finance module of the Student Portal and should raise a ticket only after the processing period has elapsed.",
    },
    {
        "rule_id": "ADM-007", "chapter": "Administrative Procedures", "section": "18.3 Grievances",
        "subsection": "General Grievances", "title": "General grievance redressal",
        "exact_text": "Non-academic grievances, including those relating to facilities and services, may be raised through the grievance module of the Student Portal. The grievance cell acknowledges each grievance within three working days and endeavours to resolve it within fifteen working days, escalating unresolved matters to the relevant administrative head.",
    },
    {
        "rule_id": "ADM-010", "chapter": "Administrative Procedures", "section": "18.4 Name and Data",
        "subsection": "Record Correction", "title": "Correction of personal records",
        "exact_text": "Requests to correct personal data such as name spelling or date of birth must be accompanied by supporting official documents and are processed by the registrar within ten working days. Corrections to academic records, such as recorded marks, follow the re-evaluation and appeals procedures rather than this administrative process.",
    },

    # ------------------------------------------------------ Additional corpus depth
    {
        "rule_id": "REG-015", "chapter": "Registration", "section": "1.4 Prerequisites",
        "subsection": "Prerequisite Enforcement", "title": "Enforcement of course prerequisites",
        "exact_text": "A student may register for a course only if all listed prerequisite courses have been passed. The Student Portal blocks registration where a prerequisite is unmet, and a waiver may be granted solely by the course instructor in writing where the student demonstrates equivalent preparation. A prerequisite waiver applies only to registration and does not exempt the student from any assessed content of the course.",
    },
    {
        "rule_id": "REG-018", "chapter": "Registration", "section": "1.5 Audit",
        "subsection": "Audit Registration", "title": "Auditing a course",
        "exact_text": "A student may register to audit a course for no credit, subject to the instructor's consent and available seats. Audited courses appear on the transcript with an 'AU' notation, carry no grade, and do not count toward the credit requirement for graduation. Audit status must be declared at the time of registration and cannot be converted to credit registration after the add-drop period.",
    },
    {
        "rule_id": "ELI-013", "chapter": "Academic Eligibility", "section": "2.5 Maximum Duration",
        "subsection": "Time Limit", "title": "Maximum time to complete the degree",
        "exact_text": "A student must complete all requirements for the undergraduate degree within a maximum of six years from the date of first registration. Periods of approved semester break are excluded from this computation. A student who does not complete the degree within the maximum permitted duration is required to seek the special permission of the Academic Council to continue.",
    },
    {
        "rule_id": "ELI-016", "chapter": "Academic Eligibility", "section": "2.6 Transfer Credit",
        "subsection": "Credit Transfer", "title": "Recognition of transfer credits",
        "exact_text": "Credits earned at a recognised institution prior to admission, or during an approved exchange, may be transferred subject to evaluation by the department. A maximum of 40 credits may be transferred toward the degree, and only courses in which a grade equivalent to 'C' or higher was earned are eligible. Transferred credits count toward graduation but are excluded from the cumulative grade point average.",
    },
    {
        "rule_id": "ATT-011", "chapter": "Attendance", "section": "3.4 Recording",
        "subsection": "Attendance Recording", "title": "Method of recording attendance",
        "exact_text": "Attendance is recorded electronically at the start of each scheduled session, and the running attendance percentage is visible to the student on the Student Portal within 48 hours. A student who believes attendance has been recorded incorrectly must raise the discrepancy with the instructor within one week of the session; corrections are not entertained after the attendance register for the semester is closed.",
    },
    {
        "rule_id": "ATT-014", "chapter": "Attendance", "section": "3.5 Laboratory Courses",
        "subsection": "Practical Attendance", "title": "Attendance in laboratory courses",
        "exact_text": "Laboratory and practical courses require completion of every scheduled experiment. A student who misses a laboratory session must complete the missed experiment in a make-up slot arranged by the laboratory in-charge before the end of the semester. Failure to complete all experiments results in an incomplete grade for the laboratory course, which must be cleared before the course can be certified as passed.",
    },
    {
        "rule_id": "EXM-014", "chapter": "Examinations", "section": "4.6 Structure",
        "subsection": "Assessment Split", "title": "Split between internal and end-semester assessment",
        "exact_text": "The final course score is composed of internal (continuous) assessment and the end-semester examination. Unless the syllabus specifies otherwise, internal assessment carries 40% and the end-semester examination carries 60% of the total marks. A student must obtain at least 30% in the end-semester examination component, independent of internal marks, to be declared as having passed the course.",
    },
    {
        "rule_id": "EXM-017", "chapter": "Examinations", "section": "4.7 Special Exams",
        "subsection": "Missed Examination", "title": "Special examination for genuine absence",
        "exact_text": "A student who is unable to appear in an end-semester examination due to hospitalisation or bereavement, supported by documentation submitted within seven days, may be permitted a special examination. The special examination is scheduled at the discretion of the examinations office and is treated as a first attempt, so the resulting grade is recorded without any supplementary notation.",
    },
    {
        "rule_id": "GRD-016", "chapter": "Grading", "section": "5.6 Incomplete",
        "subsection": "Incomplete Grade", "title": "Award and resolution of an incomplete grade",
        "exact_text": "An 'I' (incomplete) grade may be awarded where a student has completed the majority of a course but, for a documented reason, could not complete a specific component. The outstanding component must be completed within four weeks of the start of the next semester, failing which the incomplete grade is automatically converted to the grade earned on the completed components, which may be a fail.",
    },
    {
        "rule_id": "GRD-019", "chapter": "Grading", "section": "5.7 Recomputation",
        "subsection": "CGPA Recomputation", "title": "Effect of repeated courses on CGPA",
        "exact_text": "When a student repeats a course that was previously failed, only the higher of the two grades is counted in the cumulative grade point average, though both attempts remain visible on the transcript. Where a course is repeated under the grade-improvement provision after a pass, the same higher-of-two rule applies to the grade point calculation.",
    },
    {
        "rule_id": "REX-012", "chapter": "Re-examinations and Supplementary Examinations",
        "section": "6.5 Scheduling", "subsection": "Supplementary Schedule",
        "title": "Timing of supplementary examinations",
        "exact_text": "Supplementary examinations are ordinarily conducted within four to six weeks after the declaration of regular end-semester results, and always before the commencement of the next regular semester. The detailed schedule is published at least two weeks in advance. A student appearing in a supplementary examination remains registered for the next semester on a provisional basis pending the supplementary result.",
    },
    {
        "rule_id": "ASG-009", "chapter": "Assignments", "section": "7.4 Feedback",
        "subsection": "Return of Work", "title": "Return of graded assignments",
        "exact_text": "Graded assignments, together with feedback, are returned to students within two weeks of the submission deadline. Students who wish to contest an assignment mark must do so within three working days of the marks being released, after which the assignment marks are treated as final and are locked into the internal assessment record.",
    },
    {
        "rule_id": "PRJ-012", "chapter": "Project Requirements", "section": "8.5 Supervision",
        "subsection": "Supervisor Allocation", "title": "Allocation of project supervisors",
        "exact_text": "Each capstone project is assigned a faculty supervisor at the start of the final year, based on the alignment of the project theme with faculty expertise and subject to supervisor capacity. A supervisor may guide a limited number of projects each year. A change of supervisor after allocation requires the joint consent of both faculty members and the approval of the project coordinator.",
    },
    {
        "rule_id": "INT-010", "chapter": "Internships", "section": "9.4 Assessment",
        "subsection": "Internship Grading", "title": "Assessment of the internship",
        "exact_text": "The internship is graded on a pass or fail basis. A pass requires a satisfactory employer evaluation, submission of the internship report within three weeks of completion, and a departmental presentation. A student who fails the internship assessment must undertake a further internship of the prescribed minimum duration before becoming eligible to graduate.",
    },
    {
        "rule_id": "SCH-011", "chapter": "Scholarships", "section": "10.5 Need-Based Aid",
        "subsection": "Financial Need", "title": "Need-based financial assistance",
        "exact_text": "Need-based financial assistance is available to students whose family income falls below the threshold notified each year, independent of academic merit. Applications are supported by income documentation and are assessed by the financial aid committee. Need-based aid may be combined with a merit scholarship, but the combined benefit shall not exceed the full tuition for the semester.",
    },
    {
        "rule_id": "LEV-012", "chapter": "Leave", "section": "11.5 Maternity",
        "subsection": "Maternity Leave", "title": "Maternity leave for students",
        "exact_text": "A student who is expecting or has recently given birth is entitled to maternity leave of up to one semester, during which registration may be frozen without academic penalty. The period of maternity leave is excluded from the maximum duration permitted to complete the degree, and the student resumes study at the point of interruption on providing notice to the registrar.",
    },
    {
        "rule_id": "MIS-011", "chapter": "Academic Misconduct", "section": "12.5 Data Fabrication",
        "subsection": "Research Integrity", "title": "Fabrication or falsification of data",
        "exact_text": "Fabrication or falsification of data or results in project work, laboratory reports, or the capstone thesis is treated as a serious instance of academic misconduct. Where proven, the affected piece of work is annulled, and the student is required to redo it under supervision. The Academic Integrity Committee may additionally record a formal censure that is disclosed on request to external verifiers.",
    },
    {
        "rule_id": "DIS-010", "chapter": "Disciplinary Rules", "section": "13.4 Ragging",
        "subsection": "Anti-Ragging", "title": "Prohibition of ragging",
        "exact_text": "Ragging in any form is strictly prohibited and is treated as a grave disciplinary offence. A student found to have engaged in ragging is liable to immediate suspension pending inquiry and, on proof, to penalties up to and including expulsion and reporting to the authorities. The anti-ragging committee investigates every complaint on a time-bound basis.",
    },
    {
        "rule_id": "APL-009", "chapter": "Appeals", "section": "14.5 Composition",
        "subsection": "Appeal Body", "title": "Composition and decisions of the appeal body",
        "exact_text": "The appeal body comprises at least three members, none of whom were party to the original decision under appeal. The appeal body may confirm, vary, or set aside the decision, and its decision is communicated in writing with reasons. The decision of the appeal body is final within the university, subject only to any statutory external remedy available to the student.",
    },
    {
        "rule_id": "GRAD-010", "chapter": "Graduation", "section": "15.5 Convocation",
        "subsection": "Degree Conferral", "title": "Conferral of the degree at convocation",
        "exact_text": "Degrees are formally conferred at the annual convocation. A student who has met all graduation requirements but is unable to attend the convocation in person may receive the degree in absentia and collect the certificate later. The provisional degree certificate is issued within fifteen days of the final result for students who require it for employment or further study.",
    },
    {
        "rule_id": "DDL-012", "chapter": "Deadlines", "section": "16.5 Fee Deadlines",
        "subsection": "Tuition Payment", "title": "Deadline for payment of tuition fees",
        "exact_text": "Tuition and other prescribed fees for a semester must be paid before the end of the second week of the term. A student who has not paid the fees by the deadline is charged a late fee and may have Student Portal services, including result access and registration, suspended until the outstanding amount is cleared.",
    },
    {
        "rule_id": "EXC-007", "chapter": "Exceptions", "section": "17.4 Compassionate",
        "subsection": "Compassionate Consideration", "title": "Compassionate consideration in assessment",
        "exact_text": "Where a documented emergency affects a student's performance in an assessment, the student may apply for compassionate consideration within seven days of the assessment. The examinations office, on the advice of the department, may permit a deferred assessment or discount the affected component, provided this does not compromise the academic standard of the course.",
    },
    {
        "rule_id": "ADM-013", "chapter": "Administrative Procedures", "section": "18.5 Identity",
        "subsection": "Identity Cards", "title": "Issue and use of identity cards",
        "exact_text": "Every enrolled student is issued an identity card that must be carried on campus and produced on demand, including at examinations. The identity card remains the property of the university and must be surrendered on graduation or withdrawal. Loss of a card must be reported promptly so that a replacement can be issued through the registrar.",
    },
    {
        "rule_id": "ADM-016", "chapter": "Administrative Procedures", "section": "18.6 Communication",
        "subsection": "Official Communication", "title": "Official channel of communication",
        "exact_text": "The university communicates officially with students through the university-issued email account and the Student Portal. Students are deemed to have received any notice sent to these channels, and it is the student's responsibility to check them regularly. Communications sent to personal email or messaging accounts are provided as a courtesy only and are not the official record.",
    },
    {
        "rule_id": "ELI-019", "chapter": "Academic Eligibility", "section": "2.7 Minimum Load",
        "subsection": "Full-Time Status", "title": "Minimum credits for full-time status",
        "exact_text": "To retain full-time student status, and the benefits attached to it such as hostel allocation and travel concessions, a student must be registered for at least 12 credits in a regular semester. A student registered for fewer than 12 credits is classified as part-time for that semester and is assessed fees on a per-credit basis rather than the full-time rate.",
    },
    {
        "rule_id": "EXM-020", "chapter": "Examinations", "section": "4.8 Open Book",
        "subsection": "Permitted Materials", "title": "Materials permitted in open-book examinations",
        "exact_text": "In an examination designated as open book, a candidate may bring printed textbooks and handwritten notes but may not bring any electronic device, including calculators, unless the question paper expressly permits a specified model. The permitted materials for each open-book examination are announced at least one week in advance, and possession of any material beyond that list constitutes malpractice.",
    },
    {
        "rule_id": "GRD-022", "chapter": "Grading", "section": "5.8 Transcript Notation",
        "subsection": "Withheld Results", "title": "Withholding of results for dues",
        "exact_text": "The result of a student who has outstanding financial dues, unreturned library materials, or an unresolved disciplinary matter is withheld and marked as 'RW' (result withheld) until the obligation is cleared. A withheld result is not a fail; the substantive grade is released, and the transcript updated, within five working days of the obligation being discharged.",
    },
    {
        "rule_id": "PRJ-015", "chapter": "Project Requirements", "section": "8.6 Ethics",
        "subsection": "Ethics Clearance", "title": "Ethics clearance for projects involving human subjects",
        "exact_text": "A capstone project that involves human participants, personal data, or field surveys must obtain clearance from the institutional ethics committee before data collection begins. The application describes the data to be collected, the consent process, and the storage and disposal of records. Data collected without prior ethics clearance may not be used, and its inclusion is treated as a breach of research integrity.",
    },
    {
        "rule_id": "SCH-014", "chapter": "Scholarships", "section": "10.6 Conduct Condition",
        "subsection": "Good Conduct", "title": "Conduct condition attached to scholarships",
        "exact_text": "All scholarships, whether merit-based or need-based, are conditional on the recipient maintaining good conduct throughout the award period. A student against whom a disciplinary penalty of suspension or higher is imposed forfeits the scholarship for the semester in which the penalty falls, and any amount already disbursed for that semester is recoverable by the finance office.",
    },
    {
        "rule_id": "LEV-015", "chapter": "Leave", "section": "11.6 Bereavement",
        "subsection": "Bereavement Leave", "title": "Bereavement leave entitlement",
        "exact_text": "A student may avail bereavement leave of up to seven days on the death of an immediate family member. Bereavement leave is counted as attendance for the affected courses on submission of appropriate documentation, and where it coincides with a scheduled assessment, the student may apply for compassionate consideration or a deferred assessment under the exceptions chapter, and the department will make reasonable accommodation for the affected coursework.",
    },
]

# Pairs of rule_ids that DELIBERATELY conflict. Used by the evaluation harness as the
# ground truth for "expected conflicting rule ids" and documented in the README.
CONTRADICTIONS = [
    {"topic": "Minimum attendance to appear in end-semester exams (75% vs 80%)", "rules": ["ATT-002", "EXM-003"]},
    {"topic": "Number of supplementary attempts allowed per course (two vs one)", "rules": ["REX-002", "REX-006"]},
    {"topic": "Late assignment submission (5-day grace vs none)", "rules": ["ASG-003", "DDL-004"]},
    {"topic": "Medical leave entitlement per semester (15 vs 10 days)", "rules": ["LEV-002", "LEV-006"]},
    {"topic": "Minimum passing grade (D/40% vs C/50% for core)", "rules": ["GRD-003", "GRD-008"]},
    {"topic": "Grace marks to clear a course (up to 3 vs none)", "rules": ["EXM-008", "GRD-010"]},
    {"topic": "Minimum internship duration (8 vs 6 weeks)", "rules": ["INT-002", "INT-006"]},
    {"topic": "Credits required before internship (90 vs 100)", "rules": ["INT-003", "INT-007"]},
    {"topic": "Merit scholarship CGPA requirement/renewal (8.0 vs 7.5)", "rules": ["SCH-002", "SCH-005"]},
    {"topic": "Maximum project/group team size (4 vs 3)", "rules": ["PRJ-003", "PRJ-006"]},
    {"topic": "Registration completion window (2 weeks vs 10 days)", "rules": ["REG-002", "DDL-002"]},
    {"topic": "Total credits required to graduate (160 vs 156)", "rules": ["GRAD-002", "GRAD-007"]},
    {"topic": "Time limit to file an appeal (7 vs 14 days)", "rules": ["APL-002", "APL-005"]},
    {"topic": "Probation CGPA threshold (below 5.0 vs below 4.5)", "rules": ["ELI-004", "DIS-004"]},
    {"topic": "Penalty for first plagiarism offence (zero on assignment vs fail course)", "rules": ["MIS-002", "MIS-005"]},
    {"topic": "Maximum course load per semester (24 vs 27 credits)", "rules": ["REG-005", "REG-009"]},
    {"topic": "Course withdrawal deadline (week 8 vs week 10)", "rules": ["DDL-006", "EXC-004"]},
    {"topic": "Re-evaluation request window (15 vs 7 days)", "rules": ["EXM-005", "APL-006"]},
    {"topic": "Scholarship disbursement/processing time (30 vs 45 days)", "rules": ["SCH-003", "ADM-004"]},
]


def get_rules():
    return RULES


def get_rule_by_id(rule_id: str):
    for r in RULES:
        if r["rule_id"] == rule_id:
            return r
    return None


def get_chapters():
    return CHAPTERS


def corpus_stats():
    words = sum(len(r["exact_text"].split()) + len(r["title"].split()) for r in RULES)
    return {
        "total_rules": len(RULES),
        "total_chapters": len(CHAPTERS),
        "total_words": words,
        "intentional_contradictions": len(CONTRADICTIONS),
    }
