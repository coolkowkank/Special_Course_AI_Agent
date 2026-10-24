def fetch_user_transactions():
    """
    Simulates a 6-month uncategorized transaction stream designed to test:
    - LOW RISK: Basic income, rent, groceries, and utilities.
    - HIGH RISK: Lifestyle habits (luxury dining), life events (pets, travel), and goal progress (car savings).
    - BLOCKED: Medical, religious, political, and trade union affiliations.
    """
    return [
        # --- MONTH 1 (Baseline behavior) ---
        {"date": "2026-05-01", "merchant": "Vuokraovi Asunnot", "amount": -1250.00},
        {"date": "2026-05-05", "merchant": "Helen Electricity", "amount": -45.50},
        {"date": "2026-05-12", "merchant": "S-Market Helsinki", "amount": -112.50},
        {"date": "2026-05-25", "merchant": "Nordea Employer", "amount": 4200.00}, # Base salary
        {"date": "2026-05-26", "merchant": "Car Savings Account", "amount": -300.00}, # Goal tracking
        
        # --- MONTH 2 (Salary increase & union dues) ---
        {"date": "2026-06-01", "merchant": "Vuokraovi Asunnot", "amount": -1250.00},
        {"date": "2026-06-15", "merchant": "Trade Union Pro Finland", "amount": -49.00}, # SENSITIVE: Union
        {"date": "2026-06-25", "merchant": "Nordea Employer", "amount": 4800.00}, # Salary increased!
        {"date": "2026-06-26", "merchant": "Car Savings Account", "amount": -500.00}, # Increased saving
        
        # --- MONTH 3 (Travel & political donation) ---
        {"date": "2026-07-01", "merchant": "Vuokraovi Asunnot", "amount": -1250.00},
        {"date": "2026-07-10", "merchant": "Finnair Oyj", "amount": -420.00}, # HIGH RISK: Travel habit
        {"date": "2026-07-14", "merchant": "Finnish Green League Party", "amount": -50.00}, # SENSITIVE: Politics
        {"date": "2026-07-18", "merchant": "Hotel Berlin", "amount": -380.00},
        {"date": "2026-07-25", "merchant": "Nordea Employer", "amount": 4800.00},
        
        # --- MONTH 4 (New life event & religious donation) ---
        {"date": "2026-08-01", "merchant": "Vuokraovi Asunnot", "amount": -1250.00},
        {"date": "2026-08-08", "merchant": "Musti ja Mirri Pet Store", "amount": -250.00}, # HIGH RISK: New pet?
        {"date": "2026-08-15", "merchant": "Helsinki Lutheran Church", "amount": -120.00}, # SENSITIVE: Religion
        {"date": "2026-08-25", "merchant": "Nordea Employer", "amount": 4800.00},
        
        # --- MONTH 5 (Luxury dining spike & pharmacy) ---
        {"date": "2026-09-01", "merchant": "Vuokraovi Asunnot", "amount": -1250.00},
        {"date": "2026-09-12", "merchant": "Gourmet Steakhouse", "amount": -220.00}, # HIGH RISK: Dining habit
        {"date": "2026-09-15", "merchant": "Yliopiston Apteekki Pharmacy", "amount": -85.00}, # SENSITIVE: Medical
        {"date": "2026-09-20", "merchant": "Bistro Helsinki", "amount": -150.00},
        {"date": "2026-09-25", "merchant": "Nordea Employer", "amount": 4800.00},
        
        # --- MONTH 6 (Current month with major medical event) ---
        {"date": "2026-10-01", "merchant": "Vuokraovi Asunnot", "amount": -1250.00},
        {"date": "2026-10-05", "merchant": "Netflix", "amount": -15.99},
        {"date": "2026-10-18", "merchant": "Sushi San", "amount": -180.00},
        {"date": "2026-10-20", "merchant": "Helsinki Oncology Center", "amount": -450.00}, # SENSITIVE: Medical
    ]