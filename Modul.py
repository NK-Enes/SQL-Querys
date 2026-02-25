import sqlite3 as sql
import warnings

def SQL_Load (Format = None,TableName = None,Columns = None,Values = None,Distinct = None,Conditions = None,Ordering = None,Pagination = None,Grouping = None,
              Having = None,Join = None,Unions = None,ReturnType = None,DataBase = None):
    """
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
    """
    Union_Dict = {0: " UNION ",1: " UNION ALL ",2: " INTERSECT ",3: " EXCEPT "}
    def Select (TableName_DEF = None,Columns_DEF = None,Values_DEF = None,Distinct_DEF = None,Conditions_DEF = None,Grouping_DEF = None,Having_DEF = None,Join_DEF = None):
        Columns_Dict = {"*RN": "ROW_NUMBER()", "*R": "RANK()", "*DR": "DENSE_RANK()", "*NT": "NTILE({})","*SUM": "SUM({})", "*AVG": "AVG({})", "*COUNT": "COUNT(*)"}
        def Columns_Func(Columns_DEF):
            Output = []
            for Column in Columns_DEF:
                if Column.find("_") == -1:
                    Output.append(Columns_Dict.get(Column, Column))
                else:
                    Output.append(
                        Columns_Dict.get(Column[:Column.find("_")], Column).format(Column[Column.find("_") + 1:]))
            return Output

        Columns_DEF = ", ".join(Columns_Func(Columns_DEF)) if type(Columns_DEF) is list else "*"
        if Distinct:
            Draft = f"SELECT DISTINCT {Columns_DEF} FROM {TableName_DEF}"
        else:
            Draft = f"SELECT {Columns_DEF} FROM {TableName_DEF}"
        if Join_DEF is not None:
            if Join_DEF[0] == 2:  # Cross (Cartesian)
                Draft += " CROSS JOIN " + Join_DEF[1]
            else:
                JoinType = " INNER JOIN " if Join_DEF[0] == 0 else " LEFT JOIN " if Join_DEF[0] == 1 else False
                if JoinType:
                    Draft += JoinType + Join_DEF[1] + " ON " + Join_DEF[2] + " = " + Join_DEF[3]
                else:
                    warnings.warn(f"Join Type Error - ({Join[0]}) Join Types Between [0-2]")
        if Conditions_DEF is not None:
            Conditions_DEF = [Condition if type(Condition[2]) in (str, int, float) else Condition[:2] + [
                "(" + ", ".join([f"'{Acceptable}'" for Acceptable in Condition[2]]) + ")"] for Condition in Conditions_DEF]
            Conditions_DEF = [[Columns_Dict.get(Condition[0], Condition[0]), *Condition[1:]] for Condition in Conditions_DEF]
            Draft += " WHERE " + " AND ".join([("{} {} {}".format(*Condition) if type(Condition[2]) in (int,float) else "{} {} '{}'".format(*Condition)) for Condition in Conditions_DEF])
        if Grouping_DEF is not None:
            Draft += " GROUP BY " + Grouping_DEF
        if Having_DEF is not None and Grouping_DEF is not None:  # Group Must Be to Exist
            Having_DEF = [Condition if type(Condition[2]) in (str, int, float) else Condition[:2] + [
                "(" + ", ".join([f"'{Acceptable}'" for Acceptable in Condition[2]]) + ")"] for Condition in Having_DEF]
            Having_DEF = [[Columns_Dict.get(Have[0], Have), *Have[1:]] for Have in Having_DEF]
            Draft += " HAVING " + " AND ".join([("{} {} {}".format(*Condition) if type(Condition[2]) in (int,float) else "{} {} '{}'".format(*Condition)) for Condition in Having_DEF])
        elif Grouping_DEF is None and Having_DEF is not None:
            warnings.warn("Grouping Error - You Tried to RUN Having Without Grouping")
        return Draft
    if (Format is not None) and (TableName is not None):
        Format = Format.upper()
        if Format == "SELECT":
            Draft = Select(TableName_DEF=TableName,Columns_DEF=Columns,Values_DEF=Values,Distinct_DEF=Distinct,Conditions_DEF=Conditions,Grouping_DEF=Grouping,Having_DEF=Having,Join_DEF=Join)
            if Unions is not None:
                UnionType = Union_Dict.get(Unions[0],False)
                if UnionType:
                    Draft = "( " + Draft + UnionType + Select(**Unions[1]) + " ) " # Format Selected to 2. Query
            if Ordering is not None:
                Order = ", ".join([Order[0] + " " + Order[1] for Order in Ordering])
                Draft += " ORDER BY " + Order
            if Pagination is not None:
                Draft += " LIMIT " + (str(Pagination) if type(Pagination) is str else str(Pagination[0]) + " OFFSET " + str(Pagination[1]))

            con = sql.connect(DataBase)
            cursor = con.cursor()
            cursor.execute(Draft)
            DataSet = cursor.fetchall()
            if ReturnType == 0: # Raw
                return DataSet
            elif ReturnType == 1: # Empty Warning
                if DataSet is None or DataSet == [] or DataSet[0] == []:
                    return False
                else:
                    return DataSet
            elif ReturnType == 2: # One Row
                return [x[0] for x in DataSet]
            con.close()

        else:
            warnings.warn(f"Format is Incorrect You Write: '{Format}'")
            return False
    else:
        warnings.warn(f"Format or Table Name Error You Write: Format = '{Format}'\t Table Name = '{TableName}'")
        return False

