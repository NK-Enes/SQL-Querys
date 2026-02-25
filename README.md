SQL Load params
    @param Format (str): Mainly mean what you expect from the database
    @param TableName (str): Name of the table
    @param Columns (list):
        - Format is Select: The WANTED columns name
            > Have Some Functions in SQL Search:
                $ ROW_NUMBER() : *RN       $ RANK() : *R        $ DENSE_RANK() : *DR        $ NTILE(x) : *NT_x
                $ SUM(x) : *SUM_x          $ AVG(x) : *AVG_x    $ COUNT(*) : *COUNT
            > Exceptions if Columns are not specified or (str) '*' it's mean get ALL
        - Else: The Edited Columns name
    @param Values (list):
        - Format is not Select: The Value which one to edited
    @param Distinct (T/F): Removes duplicates. return list made of set's items
    @param Conditions (list (Items: list)): Add a condition check
        - Item structure: [Condition Column, Look Type (=,>,<,is,...), Value(s)] Example:["Status","=","Done"] / ["Status","in",("Done","New")]
        - Containable Logics: =, !=, <, >, <=, >=, AND, OR, IN, LIKE, BETWEEN, IS NULL
    @param Ordering (list (Items: list)): add an Order Command to Dataset
        - Item Structure: [Value, ASC/DESC] Example: ["Profit","DESC"]
    @param Pagination (int/str/list): Add a Pagination (LIMIT - OFFSET)
        - Structure: int/str: LIMIT X list: LIMIT X[0] OFFSET X[1]
    @param Grouping (str): add a Grouping Command to Dataset
        - Structure: "GROUP BY X"
    @param Having (list (Items: list)): Add a condition to Groups
        - Item structure: [Condition Column, Look Type (=,>,<,is,...), Value(s)] Example:["Status","=","Done"] / ["Status","in",("Done","New")]
        - Containable Logics: =, !=, <, >, <=, >=, AND, OR, IN, LIKE, BETWEEN, IS NULL
    @param Join (list): To Combine Tables
        - Item Structure: [Join Type, Connected Table Name, Connection Value 1, Connection Value 2]
        - Exception: if Join Type is 2 Then Mean Cross Join (Cartesian) Then Just Table
    @param Unions (dict): To Combine Results (2 Different Query)
        - Structure: Dict Contain All Value Keys as Key and Store it to Create New Query Example: {"Format": "Select","TableName": "ESS_Segment ...}

    :return: List
    @param ReturnType 0: Raw 1: Empty Free 2: One Column (Manuel Ill add a Auto)

    WORKING ON:
    - More Flexible And Fast UNION's
    - Subquery
    - CTE (With)
    - WITH RECURSIVE
    - OVER
