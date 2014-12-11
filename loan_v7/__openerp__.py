#!/usr/bin/env python
# -*- encoding: utf-8 -*-

{
    "name" : "Loan Management - TANTUMS",
    "version" : "1.0",
    "depends" : ["base", "account", "account_voucher", "report_webkit"],
    "author" : "TANTUMS",
    "description": """Loan Management System
    * Integrated to Accounting System
    * Usefull for any type of Loans - Home, Business, Personal
    * Clean Varification Process for Proofs 
    * Workflow for Loan Approval/Rejection
    * Reports related to the Loans, Documents, Loan Papers
    * Dynamic Interest Rates Calculation
    """,
    "website" : "http://www.tantums.com",
    "init_xml" : [],
     "demo_xml" : [
        "loan_demo.xml"
    ],
    "data" : [
        "views/loan_view.xml","views/loan_proof_type_view.xml","views/loan_installment_period_view.xml",
        "views/account_loan_proof_view.xml", "views/account_loan_bank_cheque_view.xml","views/account_loan_installment_view.xml",
        "sequences/loan_sequence.xml", "report/loan_report.xml","workflows/loan_workflow.xml", "report/wizard_estado_cuenta_view.xml"
    ],
    "active": False,
    "installable": True
}
