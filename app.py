import streamlit as st
from datetime import datetime

from src.validators import validate_time_string

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

INCORRECT_STRING_ERROR = (
    'Время не соответствует шаблону "%Y-%m-%dT%H:%M:%SZ". Поле ввода не должно содержать пробелов.'
    'Пример корректно введенного времени: 2024-02-14T15:11:54Z')


def generate_xml(message_data, organization_data, form_data, contract_spending_data, supplement_data, part_data, reasons_data):
    
    # Создание корневого элемента Message с атрибутами
    message = ET.Element("Message", PreviousUID=message_data['PreviousUID'], UID=message_data['UID'], CreateDate=message_data['CreateDate'])

    # Добавление элемента Organization с его атрибутами внутрь Message
    ET.SubElement(message, "Organization", ContractDate=organization_data['ContractDate'],
                  GOZUID=organization_data['GOZUID'], Name=organization_data['Name'], KPP=organization_data['KPP'],
                  INN=organization_data['INN'])
    
    # Добавление элемента Forms внутрь Message
    forms = ET.SubElement(message, "Forms")

    # Добавление элемента Form8 с его атрибутами внутрь Forms
    form8 = ET.SubElement(forms, "Form8", Quarter=form_data[1]['Quarter'], Year=form_data[1]['Year'], ReportDate=form_data[1]['ReportDate']) 
    
    # Добавление элемента ContractSpending с его атрибутами внутрь Form8
    ET.SubElement(form8, "ContractSpending", Income=contract_spending_data['Income'], Reserve=contract_spending_data['Reserve'],
                                      Other=contract_spending_data['Other'], Rates=contract_spending_data['Rates'], Taxes=contract_spending_data['Taxes'],
                                      Salary=contract_spending_data['Salary'], Total=contract_spending_data['Total'])

    # Добавление элемента Contractors.Contractor с его атрибутами внутрь Forms
    ET.SubElement(forms, "Contractors.Contractor", ContractDate=form_data[2]['ContractDate'], 
                                           Name=form_data[2]['Name'], INN=form_data[2]['INN'], Total=form_data[2]['Total'], 
                                           FinishDate=form_data[2]['FinishDate'], PaymentCurrent=form_data[2]['PaymentCurrent'],
                                           PaymentPlanned=form_data[2]['PaymentPlanned'], Cost=form_data[2]['Cost'],
                                           AccountNumber=form_data[2]['AccountNumber'], ContractNumber=form_data[2]['ContractNumber']) 
    
    # Добавление элемента PlannedPay с его атрибутами внутрь Forms
    ET.SubElement(forms, "PlannedPay", Total=form_data[3]['Total'], PaymentCurrent=form_data[3]['PaymentCurrent'],
                                PaymentPlanned=form_data[3]['PaymentPlanned']) 
    
    # Добавление элемента ContractFinance с его атрибутами внутрь Forms
    ET.SubElement(forms, "ContractFinance", DepositeIncome=form_data[4]['DepositeIncome'], 
                                    PlannedIncome=form_data[4]['PlannedIncome'], DateBalance=form_data[4]['DateBalance'],
                                    CashBalance=form_data[4]['CashBalance'], TotalRequirement=form_data[4]['TotalRequirement']) 
    
    # Добавление элемента Supplement внутрь Message
    supplement = ET.SubElement(message, "Supplement", ReportDate=supplement_data['ReportDate'])

    # Добавление элемента Parts внутрь Supplement
    parts = ET.SubElement(supplement, "Parts")

    # Добавление элемента Parts внутрь Supplement
    part = ET.SubElement(parts, "Part", Quarter=part_data['Quarter'], Year=part_data['Year'], Deviation=part_data['Deviation'], Requirement=part_data['Requirement'] )

    # Добавление элемента Reasons внутрь Part
    ET.SubElement(part, "Reasons", Reason=reasons_data['Reason'] )

    
    # Построение строки XML из дерева ET
    rough_string = ET.tostring(message, 'utf-8')
    reparsed = parseString(rough_string)

    # Возвращаем красиво отформатированную XML строку
    return reparsed.toprettyxml(indent="  ")


# Функция для инициализации состояния сеанса. Сюда по сути нужно пихать только даты, т.к они обновляют состояние
# приложения
def init_session_state():
    if 'CreateDate' not in st.session_state:
        st.session_state.CreateDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'ContractDate' not in st.session_state:
        st.session_state.ContractDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'ReportDate' not in st.session_state:
        st.session_state.ReportDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'FinishDate' not in st.session_state:
        st.session_state.FinishDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'DateBalance' not in st.session_state:
        st.session_state.DateBalance = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'ReportDate' not in st.session_state:
        st.session_state.ReportDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 

def message_form():
    st.write('## Message')
    # Именование не соответствует правилам, но в силу сжатых сроков для удобства - просто копипаст из xml
    PreviousUID = st.text_input('PreviousUID',
                                '0',
                                help='Всегда 0')
    UID = st.text_input('UID',
                        '0',
                        help='help')
    # Используем значения из состояния сеанса
    CreateDate = st.text_input('CreateDate', st.session_state.CreateDate, help='Дата создания документа')
    if not validate_time_string(CreateDate):
        st.error(INCORRECT_STRING_ERROR)
    else:
        st.session_state.CreateDate = CreateDate  # Обновляем состояние сеанса при валидном вводе

    return {'PreviousUID': PreviousUID, 'UID': UID, 'CreateDate': CreateDate}


def organization_form():
    st.write('## Organization')
    ContractDate = st.text_input('ContractDate', st.session_state.ContractDate, help='В формате 2023-12-15T00:00:00Z')
    if not validate_time_string(ContractDate):
        st.error(INCORRECT_STRING_ERROR)
    else:
        st.session_state.ContractDate = ContractDate  # Обновляем состояние сеанса при валидном вводе
    GOZUID = st.text_input('GOZUID', '', help='игК')
    Name = st.text_input('Name', '', help='help')
    KPP = st.text_input('KPP', '', help='help')
    INN = st.text_input('INN', '', help='help')
    return {'ContractDate': ContractDate, 'GOZUID': GOZUID, 'Name': Name, 'KPP': KPP, 'INN': INN}

def form_form():
    st.write('## Form')
    
    Type = st.text_input('Type', '8', help='Для данной формы принимается значение 8')
    
    return {'Type': Type}

def form8_form():
    st.write('## Form8')
    
    Quarter = st.text_input('Quarter', '', help='help')
    Year = st.text_input('Year', '', help='help')
    ReportDate = st.text_input('ReportDate', st.session_state.ReportDate, help='В формате 2024-01-01T00:00:00Z') 
    
    return {'Quarter': Quarter, 'Year': Year, 'ReportDate': ReportDate }

def contract_spending_form():
    st.write('## ContractSpending')

    Income = st.text_input('Income', '', help='Указывается в копейках')
    Reserve = st.text_input('Reserve', '', help='Указывается в копейках')
    Other = st.text_input('Other', '', help='Указывается в копейках')
    Rates = st.text_input('Rates', '', help='Указывается в копейках')
    Taxes = st.text_input('Taxes', '', help='Указывается в копейках')
    Salary = st.text_input('Salary', '', help='Указывается в копейках')
    Total = st.text_input('Total', '', help='Указывается в копейках')
    
    return {'Income': Income, 'Reserve': Reserve, 'Other': Other, 'Rates': Rates, 'Taxes': Taxes, 'Salary': Salary, 'Total': Total }

def contractors_contractor_form():
    st.write('## Contractors.Contractor')

    ContractDate = st.text_input('ContractDate', st.session_state.ContractDate, help='В формате 2001-01-01T00:00:00Z')
    Name = st.text_input('Name', key="Contractors_Name", value = '', help='help')
    INN = st.text_input('INN', key="Contractors_INN", value = '', help='help')
    Total = st.text_input('Total', key="Contractors_Total", value ='', help='help')
    FinishDate = st.text_input('FinishDate', st.session_state.FinishDate, help='В формате 2001-01-01T00:00:00Z')
    PaymentCurrent = st.text_input('PaymentCurrent', '', help='help')
    PaymentPlanned = st.text_input('PaymentPlanned', '', help='help')
    Cost = st.text_input('Cost', '', help='help')
    AccountNumber = st.text_input('AccountNumber', '', help='help')
    ContractNumber = st.text_input('ContractNumber', '', help='help')
    
    return {'ContractDate': ContractDate, 'Name': Name, 'INN': INN, 'Total': Total, 'FinishDate': FinishDate, 'PaymentCurrent': PaymentCurrent, 
            'PaymentPlanned': PaymentPlanned, 'Cost': Cost, 'AccountNumber': AccountNumber, 'ContractNumber': ContractNumber }

def planned_pay_form():
    st.write('## PlannedPay')

    Total = st.text_input('Total', key="PlannedPay_Total", value ='', help='help')
    PaymentCurrent = st.text_input('PaymentCurrent', key="PlannedPay_PaymentCurrent", value ='', help='help')
    PaymentPlanned = st.text_input('PaymentPlanned', key="PlannedPay_PaymentPlanned",  value ='', help='help')
    
    return { 'Total': Total, 'PaymentCurrent': PaymentCurrent, 'PaymentPlanned': PaymentPlanned }

def contract_finance_form():
    st.write('## ContractFinance')

    DepositeIncome = st.text_input('DepositeIncome', '', help='help')
    PlannedIncome = st.text_input('PlannedIncome', '', help='help')
    DateBalance = st.text_input('DateBalance', st.session_state.DateBalance, help='В формате 2024-02-08T00:00:00Z')
    CashBalance = st.text_input('CashBalance', '', help='help')
    TotalRequirement = st.text_input('TotalRequirement', '', help='Указывается в копейках')

    return { 'DepositeIncome': DepositeIncome, 'PlannedIncome': PlannedIncome, 'DateBalance': DateBalance, 'CashBalance': CashBalance, 'TotalRequirement': TotalRequirement }

def supplement_form():
    st.write('## Supplement')

    ReportDate = st.text_input('ReportDate', st.session_state.ReportDate, help='В формате 2024-02-09T00:00:00Z')

    return { 'ReportDate': ReportDate }

def part_form():
    st.write('## Part')
    
    Quarter = st.text_input('Quarter', key="Part_Quarter", value ='', help='help')
    Year = st.text_input('Year', key="Part_Year", value ='', help='help')
    Deviation = st.text_input('Deviation', '', help='help')
    Requirement = st.text_input('Requirement', '', help='help')
    
    return {'Quarter': Quarter, 'Year': Year, 'Deviation': Deviation, 'Requirement': Requirement }

def reasons_form():
    st.write('## Reasons')
    
    Reason = st.text_input('Reason', '', help='help')
    
    return {'Reason': Reason }

def main():
    init_session_state()  # Инициализируем состояние сеанса

    st.title('XML Template Filler')

    Message = message_form()
    Organization = organization_form()
    #generate_xml может принимать только 10 аргументов, поэтому элементы Form объединены в список
    Form = [form_form(), form8_form(), contractors_contractor_form(), planned_pay_form(), contract_finance_form() ] 
    ContractSpending = contract_spending_form()
    Supplement = supplement_form()
    Part = part_form()
    Reasons = reasons_form()
 
    if st.button('Generate XML'):
        xml_data = generate_xml(Message, Organization, Form, ContractSpending, Supplement, Part, Reasons)
        st.text_area("Generated XML", xml_data, height=300)


if __name__ == '__main__':
    main()
