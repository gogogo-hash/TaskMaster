import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import scrolledtext
import pyodbc
import itertools as it
import functools
from collections import defaultdict


############# MODEL - OBSERVABLE
class Observable:
    def __init__(self,
                 userID=None,
                 IDIR=None,
                 ticket_number=None,
                 user_tickets=None,
                 current_record=None,
                 current_write_table=None,
                 current_tbl_datatypes=None,
                 ref_tasktypelink=None,
                 write_ref_tblWTDWorkItems=None,
                 rev_write_ref_tblWTDWorkItems=None,
                 ref_table_workitem_constraints=None,
                 rev_ref_table_workitem_constraints=None,
                 # ticket_reference_write=None,
                 query_result=False):

        self.userID = userID
        self.IDIR = IDIR
        self.ticket_number = ticket_number
        self.user_tickets = user_tickets
        self.current_record = current_record

        self.current_write_table = current_write_table
        self.current_tbl_datatypes = current_tbl_datatypes
        self.ref_tasktypelink = ref_tasktypelink
        self.write_ref_tblWTDWorkItems = write_ref_tblWTDWorkItems
        self.rev_write_ref_tblWTDWorkItems = rev_write_ref_tblWTDWorkItems
        self.ref_table_workitem_constraints = ref_table_workitem_constraints
        self.rev_ref_table_workitem_constraints = rev_ref_table_workitem_constraints
        # self.ticket_reference_write = ticket_reference_write

        self.query_result = query_result

        self.callbacks = {}

    def add_callback(self, call_id, func):
        self.callbacks[call_id] = func

    def del_callback(self, func):
        del self.callbacks[func]

    def _do_callbacks(self, func_id):
        self.callbacks[func_id]()

    def set_userID(self, data):
        self.userID = data

    def set_IDIR(self, data):
        self.IDIR = data
        self._do_callbacks("call_IDIR")

    def set_ticket_number(self, data):
        self.ticket_number = data
        self._do_callbacks("call_ticket_number")

    def set_user_tickets(self, header_data, user_tickets):
        self.user_tickets = header_data, user_tickets
        self._do_callbacks("call_user_tickets")

    def set_current_record(self, data):
        self.current_record = data
        self._do_callbacks("call_current_record")

    def set_write_ref_tblWTDWorkItems(self, data):
        self.write_ref_tblWTDWorkItems = data
        # self._do_callbacks("call_write_ref_tblWTDWorkItems")

    def set_rev_write_ref_tblWTDWorkItems(self, data):
        self.rev_write_ref_tblWTDWorkItems = data
        # self._do_callbacks("call_rev_write_ref_tblWTDWorkItems")

    def set_ref_table_workitem_constraints(self, data):
        self.ref_table_workitem_constraints = data
        # self._do_callbacks("call_rev_write_ref_tblWTDWorkItems")

    def set_rev_ref_table_workitem_constraints(self, data):
        self.rev_ref_table_workitem_constraints = data
        # self._do_callbacks("call_rev_write_ref_tblWTDWorkItems")

    def set_current_tbl_datatypes(self, data):
        self.current_tbl_datatypes = data
        try:
            self._do_callbacks("call_current_tbl_datatypes")
        except KeyError:
            print('no callback subscribed')

    def set_ref_tasktypelink(self, data):
        self.ref_tasktypelink = data
        self._do_callbacks("call_ref_tasktypelink")

    def set_current_write_table(self, data):
        self.current_write_table = data
        self._do_callbacks("call_current_write_table")

    def set_query_result(self, query_result):
        self.query_result = query_result
        self._do_callbacks("call_query_result")

    # def set_ticket_reference_write(self, data):
    #     self.ticket_reference_write = data
    #     self._do_callbacks("call_ticket_reference_write")

    def get(self, request=None):
        if request == "userID":
            return self.userID
        elif request == "IDIR":
            return self.IDIR
        elif request == "USER_TICKETS":
            return self.user_tickets
        elif request == "write_ref_tblWTDWorkItems":
            return self.write_ref_tblWTDWorkItems
        elif request == "rev_write_ref_tblWTDWorkItems":
            return self.rev_write_ref_tblWTDWorkItems
        elif request == "ref_table_workitem_constraints":
            return self.ref_table_workitem_constraints
        elif request == "rev_ref_table_workitem_constraints":
            return self.rev_ref_table_workitem_constraints
        elif request == "current_tbl_datatypes":
            return self.current_tbl_datatypes
        elif request == "current_write_table":
            return self.current_write_table
        elif request == "ref_tasktypelink":
            return self.ref_tasktypelink
        elif request == "current_record":
            return self.current_record
        elif request == "ticket_number":
            return self.ticket_number
        elif request == "query_result":
            return self.query_result
        # elif request == "ticket_reference_write":
        #     return self.ticket_reference_write
        else:
            return None


############# MODEL - DATA CLEANSING
class Data_Cleansing:

    def ticket_headers(self, data):
        headers = data
        headers_list = []
        for item in headers:
            headers_list.append(item[0])
        return headers_list

    def ticket_data(self, data):
        ticket = data
        ticket_list = []
        for row in ticket:
            for item in row:
                ticket_list.append(item)
        return ticket_list

    def create_dict(self, headers, data):
        dict_a = {}
        for f, b in it.zip_longest(headers, data):
            dict_a[f] = b
        return dict_a

    def create_dict_appendedlistvalues(self, data):
        dict_a = defaultdict(list)
        for row in data:
            dict_a[row[0]].append(row[1])
        return dict_a

    def nested_dict(self, data, x=0, y=1, z=2):
        dict_b = defaultdict(list)
        dict_a = defaultdict(dict)
        # dict_a = dict_c[dict_b]
        # print(data)
        print(dict_a)
        for row in data:
            # dict_b[row[y]].append(row[z])
            dict_a[row[x]] = defaultdict(list)  # = dict_b[row[y]].append(row[z])
            # print(dict_a)
        # dict_b["key"] = ["value"]
        for key, value in dict_a.items():
            for row in data:
                if row[x] == key:
                    value[row[y]].append(row[z])
        for key, value in dict_a.items():
            for key2, value2 in value.items():
                print(key, key2, value2)
        print(dict_a)
        return dict_a

    def load_user_updates(self, data, model_dict):
        dict_a = {}
        output = []
        print("data: ", data)
        print("model: ", model_dict)
        print("len model:", len(model_dict))
        print("len model: ", len(model_dict.keys()))
        r = range(len(model_dict))
        for i in r:
            print(i)

        for key, value in data.items():
            if key in model_dict:
                dict_a[model_dict[key]] = value
        for i in range(len(model_dict)):
            output.append(dict_a[i])

        print(output)
        return output


############# MODEL
class Model:
    def __init__(self):
        self.myQuery = Observable()
        self.data_cleansing = Data_Cleansing()
        self.ticket_reference_update = {"XRefSerialNumber": 0, "Owner": 1, "Deadline": 2, "Description": 3, "Status": 4,
                                        "Client": 5, "Priority": 6, "Task": 7, "Tasktype": 8, "SupportedSystem": 9,
                                        "Conclusion": 10, "LastEditedBy": 11, "CSID": 12, "Notes": 13,
                                        "DateCompleted": 14, "TicketNumber": 15}
        self.ticket_reference_write = {"XRefSerialNumber": 0, "Owner": 1, "Deadline": 2, "Description": 3, "Status": 4,
                                       "Client": 5, "Priority": 6, "Task": 7, "Tasktype": 8, "SupportedSystem": 9,
                                       "Conclusion": 10, "LastEditedBy": 11, "CSID": 12, "Notes": 13,
                                       "DateCompleted": 14}
        self.ticket_write_fields = {"XRefSerialNumber": None, "Owner": None, "Deadline": None, "Description": None,
                                    "Notes": None, "Status": None, "Client": None, "Priority": None, "Task": None,
                                    "Tasktype": None, "SupportedSystem": None, "Conclusion": None, "CSID": None,
                                    "LastEditedBy": None, "DateCompleted": None}
        # self.myQuery.set_ticket_reference_write(self.ticket_reference_write)

    # Grouped Functions
    def current_write_table(self, table_name=None):
        if table_name == "tblWTDWorkItems":
            self.myQuery.set_current_write_table(table_name)
            self.ref_table_tblWTDWorkItems()
            self.ref_datatypes(table_name=table_name)
            self.ref_tblTaskTypeLinkmm()
            self.ref_table_workitem_constraints()

    # Core functions
    def ref_table_workitem_constraints(self):
        sql = """
                SELECT
                'Priority' AS fk_name,
                p.PriorityID as ID,
                p.PriorityDescription as decode_value
                FROM
                tluWTDPriority p

                UNION

                SELECT
                'Owner' AS fk_name,
                o.UserId,
                o.IDIR
                FROM
                tblWTDOwner o

                UNION

                SELECT
                'Client' as fk_name,
                c.ClientID,
                c.ClientName
                FROM
                tblWTDClients c

                UNION

                Select
                'CSID' as fk_name,
                cs.CSID,
                cs.CSDescription
                FROM
                tblCompletionStatus cs

                UNION

                SELECT
                'Conclusion' as fk_name,
                con.ConclusionID,
                con.ConclusionDescription
                FROM
                tluWTDConclusion con

                UNION

                SELECT
                'SupportedSystem' as fk_name,
                ss.SSID,
                ss.SystemName
                FROM
                tluWTDSupportedSystems ss

                UNION

                SELECT
                'Task' as fk_name,
                t1.TaskID,
                t1.TaskDescription
                FROM
                tluWTDTasks t1

                UNION

                SELECT
                'Tasktype' as fk_name,
                tt.TaskTypeID,
                tt.TaskType as TaskTypeDescription
                FROM
                tluWTDTaskType tt

                UNION

                SELECT
                'Status' as fk_name,
                s.StatusID,
                s.StatusDescription
                FROM
                tluWTDStatus s"""

        _, metadata = self.runQuery(sql=sql, receive=True, )
        metadata_dict = self.data_cleansing.nested_dict(metadata)
        rev_metadict = self.data_cleansing.nested_dict(metadata, x=0, y=2,
                                                       z=1)  # this is bad and should be fixed. The objects should be properly encapsulated. though, the entire architecture needs to be rewritten to follow the strategy pattern.
        self.myQuery.set_ref_table_workitem_constraints(metadata_dict)
        self.myQuery.set_rev_ref_table_workitem_constraints(rev_metadict)

    def ref_table_tblWTDWorkItems(self):
        sql = """
                SELECT
                'Priority' AS fk_name,
                p.PriorityID as ID,
                p.PriorityDescription as decode_value
                FROM
                tluWTDPriority p
                WHERE
                p.DateActivated < GETDATE() AND
                (p.DateDeactivated > GETDATE() OR
                p.DateDeactivated IS NULL)

                UNION

                SELECT
                'Owner' AS fk_name,
                o.UserId,
                o.IDIR
                FROM
                tblWTDOwner o
                WHERE
                o.DateUserActivated < GETDATE() AND
                (o.DateUserDeactivated > GETDATE() OR
                o.DateUserDeactivated IS NULL)

                UNION

                SELECT
                'Client' as fk_name,
                c.ClientID,
                c.ClientName
                FROM
                tblWTDClients c
                WHERE
                c.DateActivated < GETDATE() AND
                (c.DateDeactivated > GETDATE() OR
                c.DateDeactivated IS NULL)

                UNION

                Select
                'CSID' as fk_name,
                cs.CSID,
                cs.CSDescription
                FROM
                tblCompletionStatus cs
                WHERE
                cs.CSDateActivated < GETDATE() AND
                (cs.CSDateDeactivated > GETDATE() OR
                cs.CSDateDeactivated IS NULL)

                UNION

                SELECT
                'Conclusion' as fk_name,
                con.ConclusionID,
                con.ConclusionDescription
                FROM
                tluWTDConclusion con
                WHERE
                con.DateActivated < GETDATE() AND
                (con.DateDeactivated > GETDATE() OR
                con.DateDeactivated IS NULL)

                UNION

                SELECT
                'SupportedSystem' as fk_name,
                ss.SSID,
                ss.SystemName
                FROM
                tluWTDSupportedSystems ss
                WHERE
                ss.DateActivated < GETDATE() AND
                (ss.DateDeactivated > GETDATE() OR
                ss.DateDeactivated IS NULL)

                UNION

                SELECT
                'Task' as fk_name,
                t1.TaskID,
                t1.TaskDescription
                FROM
                tluWTDTasks t1
                WHERE
                t1.DateActivated < GETDATE() AND
                (t1.DateDeactivated > GETDATE() OR
                t1.DateDeactivated IS NULL)

                UNION

                SELECT
                'Tasktype' as fk_name,
                tt.TaskTypeID,
                tt.TaskType as TaskTypeDescription
                FROM
                tluWTDTaskType tt
                WHERE
                tt.DateActivated < GETDATE() AND
                (tt.DateDeactivated > GETDATE() OR
                tt.DateDeactivated IS NULL)

                UNION

                SELECT
                'Status' as fk_name,
                s.StatusID,
                s.StatusDescription
                FROM
                tluWTDStatus s
                WHERE
                s.DateActivated < GETDATE() AND
                (s.DateDeactivated > GETDATE() OR
                s.DateDeactivated IS NULL)"""
        _, metadata = self.runQuery(sql=sql, receive=True, )
        metadata_dict = self.data_cleansing.nested_dict(metadata)
        rev_metadict = self.data_cleansing.nested_dict(metadata, x=0, y=2,
                                                       z=1)  # this is bad and should be fixed. The objects should be properly encapsulated. though, the entire architecture needs to be rewritten to follow the strategy pattern.
        self.myQuery.set_write_ref_tblWTDWorkItems(metadata_dict)
        self.myQuery.set_rev_write_ref_tblWTDWorkItems(rev_metadict)

    def ref_datatypes(self, table_name):
        sql = """
                SELECT
                TABLE_NAME, 
                COLUMN_NAME, 
                DATA_TYPE
                FROM
                INFORMATION_SCHEMA.COLUMNS
                WHERE
                TABLE_NAME = ?"""
        _, ref_datatypes = self.runQuery(sql=sql, data=table_name, receive=True)
        self.myQuery.set_current_tbl_datatypes(ref_datatypes)

    def ref_tblTaskTypeLinkmm(self):
        sql = """
                SELECT
                t.TaskDescription,
                tt.TaskType
                FROM
                tblTaskTypeLinkmm tl
                JOIN
                tluWTDTasks as t ON
                t.TaskID = tl.TaskID AND
                t.DateActivated < GETDATE() AND
                (t.DateDeactivated > GETDATE() OR
                t.DateDeactivated IS NULL)

                JOIN
                tluWTDTaskType tt ON
                tt.TaskTypeID = tl.TypeID AND
                tt.DateActivated < GETDATE() AND
                (tt.DateDeactivated > GETDATE() OR
                tt.DateDeactivated IS NULL)

                WHERE
                tl.DateActivated < GETDATE() AND
                (tl.DateDeactivated > GETDATE() OR
                tl.DateDeactivated IS NULL)"""

        _, ref_tasktypelink = self.runQuery(sql=sql, receive=True)
        print(ref_tasktypelink)
        ref_tasktypelink = self.data_cleansing.create_dict_appendedlistvalues(data=ref_tasktypelink)
        print(ref_tasktypelink)
        self.myQuery.set_ref_tasktypelink(ref_tasktypelink)

    def write_template(self):
        self.myQuery.set_ticket_number(None)
        self.myQuery.set_current_record(self.ticket_write_fields)
        self.myQuery.set_query_result(query_result=True)

    def ticket_data(self, ticket_number=None):
        if ticket_number:
            sql = """
                        SELECT
                        wi.DateCreated,
                        wi.XRefSerialNumber,
                        o.IDIR as Owner,
                        wi.Deadline,
                        wi.Description,
                        wi.Notes,
                        wi.DateCompleted,
                        s.StatusDescription as Status,
                        c.ClientName as Client,
                        p.PriorityDescription as Priority,
                        t.TaskDescription as Task,
                        tt.TaskType as Tasktype,
                        ss.SystemName as SupportedSystem,
                        con.ConclusionDescription as Conclusion,
                        cs.CSDescription as CSID,
                        wi.TicketNumber

                        FROM
                        tblWTDWorkItems wi

                        JOIN tluWTDTasks t ON
                        wi.Task = t.TaskID

                        JOIN tluWTDTaskType tt ON
                        wi.Tasktype = tt.TaskTypeID

                        JOIN tluWTDSupportedSystems ss ON
                        wi.SupportedSystem = ss.SSID

                        JOIN tblWTDOwner o ON
                        wi.Owner = o.UserID

                        JOIN tblWTDClients c ON
                        wi.Client = c.ClientID

                        JOIN tluWTDPriority p ON
                        wi.Priority = p.PriorityID

                        JOIN tblCompletionStatus cs ON
                        wi.CSID = cs.CSID

                        JOIN tluWTDStatus s ON
                        wi.Status = s.StatusID

                        JOIN tluWTDConclusion con ON
                        wi.Conclusion = con.ConclusionID

                        WHERE
                        wi.TicketNumber = ?"""
            headers, ticket_data = self.runQuery(sql=sql, data=ticket_number,
                                                 receive=True)  # Raise exception when ticket_data = None. This feeds back to the controller indicating ticket does not exist...hopefully
        else:
            sql = """
                        SELECT
                        wi.DateCreated,
                        wi.XRefSerialNumber,
                        wi.Owner,
                        wi.Deadline,
                        wi.Description,
                        wi.Notes,
                        wi.DateCompleted,
                        wi.Status,
                        wi.Client,
                        wi.Priority,
                        wi.Task,
                        wi.Tasktype,
                        wi.SupportedSystem,
                        wi.Conclusion,
                        wi.CSID,
                        wi.TicketNumber

                        FROM
                        tblWTDWorkItems wi

                        WHERE
                        wi.TicketNumber = 1"""
            headers, ticket_data = self.runQuery(sql=sql, receive=True)
        if not ticket_data:
            # self.myQuery.set_ticket_number(ticket_number) # implement this only if the view is refreshed and data is cleared from the model.
            self.myQuery.set_query_result(query_result=False)
        else:
            headers = self.data_cleansing.ticket_headers(headers)
            ticket_data = self.data_cleansing.ticket_data(ticket_data)
            ticket_dict = self.data_cleansing.create_dict(headers, ticket_data)

            self.myQuery.set_ticket_number(ticket_number)
            self.myQuery.set_current_record(ticket_dict)
            self.myQuery.set_query_result(query_result=True)

    def validate_username(self, login_data=None, password=None):
        sql = """
                SELECT 
                    UserID,
                    IDIR
                FROM tblWTDOwner 
                WHERE 
                    IDIR = ? AND
                    Password = ? AND
                    DateUserActivated <= GETDATE() AND
                    (DateUserDeactivated >= GETDATE() OR
                        DateUserDeactivated IS NULL)
                """
        _, user_data = self.runQuery(sql, login_data, receive=True)
        userID, IDIR = user_data[0]

        self.myQuery.set_userID(userID)
        self.myQuery.set_IDIR(IDIR)

    def load_user_tickets(self, userID=None):
        if not userID:
            userID = self.myQuery.userID

        get_ticket_info_query = """
                                    SELECT TOP 100
                                    wi.DateCreated as "Date Opened",
                                    wi.TicketNumber as "Ticket Number",
                                    wi.Description as Description,
                                    t.TaskDescription as Task,
                                    tt.TaskType as "Task Type",
                                    ss.SystemName as "Supported System",
                                    o.IDIR as IDIR,
                                    c.ClientName as Client,
                                    wi.XRefSerialNumber as xReference,
                                    wi.Deadline as "Preferred Date",
                                    p.PriorityDescription as Priority,
                                    cs.CSDescription as Progress,
                                    s.StatusDescription as Status

                                    FROM
                                    tblWTDWorkItems wi

                                    JOIN tluWTDTasks t ON
                                    wi.Task = t.TaskID

                                    JOIN tluWTDTaskType tt ON
                                    wi.Tasktype = tt.TaskTypeID

                                    JOIN tluWTDSupportedSystems ss ON
                                    wi.SupportedSystem = ss.SSID

                                    JOIN tblWTDOwner o ON
                                    wi.Owner = o.UserID

                                    JOIN tblWTDClients c ON
                                    wi.Client = c.ClientID

                                    JOIN tluWTDPriority p ON
                                    wi.Priority = p.PriorityID

                                    JOIN tblCompletionStatus cs ON
                                    wi.CSID = cs.CSID

                                    JOIN tluWTDStatus s ON
                                    wi.Status = s.StatusID

                                    WHERE
                                    wi.Owner = ? AND
                                    s.StatusDescription <> 'Closed'

                                    ORDER BY wi.DateCreated desc"""

        headers, ticket_data = self.runQuery(sql=get_ticket_info_query,
                                             data=userID,
                                             receive=True)

        headers = self.data_cleansing.ticket_headers(headers)

        self.myQuery.set_user_tickets(headers, ticket_data)

    # Work in progress, critical functions required:
    def update_ticket(self, user_updates):
        ticket_data = self.data_cleansing.load_user_updates(user_updates, self.ticket_reference_update)
        print("ticket data: ", ticket_data)

        update_ticket_stmt = """
        UPDATE 
        tblWTDWorkItems 

        SET 
        XRefSerialNumber = ?, Owner = ?, Deadline = ?, Description = ?, Status = ?, Client = ?, Priority = ?, Task = ?, 
        Tasktype = ?, SupportedSystem = ?, Conclusion = ?, LastEditedBy = ?, LastEdited = GETDATE(), CSID = ?, Notes = ?,
        DateCompleted = ?


        WHERE 
        TicketNumber = ?"""

        self.runQuery(sql=update_ticket_stmt,
                      data=ticket_data,
                      receive=False)

    def add_ticket(self, user_updates):
        ticket_data = self.data_cleansing.load_user_updates(user_updates, self.ticket_reference_write)
        print(ticket_data)
        insert_ticket_stmt = """
        INSERT INTO 
        tblWTDWorkItems(DateCreated, XRefSerialNumber, Owner, Deadline, Description, Status, Client, Priority, Task, 
        Tasktype, SupportedSystem, Conclusion, LastEditedBy, LastEdited, CSID, Notes, DateCompleted) 
        OUTPUT Inserted.TicketNumber
        VALUES(GETDATE(),?,?,?,?,?,?,?,?,?,?,?,?,GETDATE(),?,?,?)"""
        _, Ticket_Number = self.writeQuery(sql=insert_ticket_stmt,
                                           data=ticket_data)

        return (Ticket_Number[0][0])

    # runQuery


    def runQuery(self, sql, data=None, receive=False, set_func=None, column_names=False):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=localhost;'
                              'DATABASE=BATMANTest07;'
                              'TrustServerCertificate=Yes;'
                              'Authentication=ActiveDirectoryIntegrated')

        cursor = conn.cursor()
        try:
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

            if receive:
                return cursor.description, cursor.fetchall()

            else:
                conn.commit()
            conn.close()
        except pyodbc.IntegrityError:
            conn.close()

    def writeQuery(self, sql, data=None):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=localhost;'
                              'DATABASE=BATMANTest07;'
                              'TrustServerCertificate=Yes;'
                              'Authentication=ActiveDirectoryIntegrated')

        try:
            cursor = conn.cursor()
            cursor.execute(sql, data)
            ticket_number = cursor.description, cursor.fetchall()
            conn.commit()
            conn.close()
            return ticket_number
        except pyodbc.IntegrityError:
            conn.close()

class Query:
    def __init__(self):
        self.dbConnection = None
        self.sql = None
        self.output = None

    def set_dbConnection(self, dbConnection):
        self.dbConnection = dbConnection

    def set_sql(self, sql):
        self.sql = sql

    def outputBehaviour(self, data):
        raise NotImplementedError

    def runQuery(self):
        conn = self.dbConnection
        try:
            cursor = conn.cursor()
            cursor.execute(self.sql)
            output = cursor.description, cursor.fetchall()
            conn.commit()
            conn.close()
            self.output = self.outputBehaviour(output)

        except pyodbc.IntegrityError:
            print("error")
        finally:
            conn.close()

    def handleOutput(self):
        print(self.output)


class Query1(Query):
    def __init__(self):
        super().__init__()
        self.dbConnection = TestDB()
        self.outputBehaviour = Output()
        self.sql = GetUserTickets()


class OutputBehaviour:
    def output(self, data):
        raise NotImplementedError


class Output(OutputBehaviour):
    def output(self, data):
        return data


class NoOutput(OutputBehaviour):
    def output(self, data):
        pass


class DBConnection:
    def __init__(self):
        self.conn = None

class TestDB(DBConnection):
    def __init__(self):
        super().__init__()
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                   'SERVER=localhost;''DATABASE=BATMANTest07;'
                                   'TrustServerCertificate=Yes;'
                                   'Authentication=ActiveDirectoryIntegrated')


class SqlStatement:
    def __init__(self):
        self.sqlStatement = None
        self.inputData = None

    def set_sqlStatement(self, sqlStatement):
        self.sqlStatement = sqlStatement

    def set_inputData(self, inputData):
        self.inputData = inputData

    def createSqlStatement(self):
        if self.inputData:
            return self.sqlStatement, self.inputData
        else:
            return self.sqlStatement


class GetUserTickets(SqlStatement):
    def __init__(self):
        super().__init__()
        self.sqlStatement = """
                                    SELECT TOP 100
                                    wi.DateCreated as "Date Opened",
                                    wi.TicketNumber as "Ticket Number",
                                    wi.Description as Description,
                                    t.TaskDescription as Task,
                                    tt.TaskType as "Task Type",
                                    ss.SystemName as "Supported System",
                                    o.IDIR as IDIR,
                                    c.ClientName as Client,
                                    wi.XRefSerialNumber as xReference,
                                    wi.Deadline as "Preferred Date",
                                    p.PriorityDescription as Priority,
                                    cs.CSDescription as Progress,
                                    s.StatusDescription as Status

                                    FROM
                                    tblWTDWorkItems wi

                                    JOIN tluWTDTasks t ON
                                    wi.Task = t.TaskID

                                    JOIN tluWTDTaskType tt ON
                                    wi.Tasktype = tt.TaskTypeID

                                    JOIN tluWTDSupportedSystems ss ON
                                    wi.SupportedSystem = ss.SSID

                                    JOIN tblWTDOwner o ON
                                    wi.Owner = o.UserID

                                    JOIN tblWTDClients c ON
                                    wi.Client = c.ClientID

                                    JOIN tluWTDPriority p ON
                                    wi.Priority = p.PriorityID

                                    JOIN tblCompletionStatus cs ON
                                    wi.CSID = cs.CSID

                                    JOIN tluWTDStatus s ON
                                    wi.Status = s.StatusID

                                    WHERE
                                    wi.Owner = ? AND
                                    s.StatusDescription <> 'Closed'

                                    ORDER BY wi.DateCreated desc"""


###############  VIEW  ######################
class View(tk.Tk):
    def __init__(self):
        super().__init__()

        self.user_inputs = {}
        self.widget_text = {}
        self.generated_canvases = {}

        self.title("BATMAN Application")
        self.geometry("900x900")

        self.main_canvas = tk.Canvas(self)
        self.zone_2 = tk.Canvas(self)
        self.zone_3 = tk.Canvas(self)
        self.zone_4 = tk.Canvas(self)

        self.main_canvas.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.zone_2.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.zone_3.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.zone_4.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)

        # MAIN CANVAS WIDGETS #
        self.user_select_label = tk.Label(self.main_canvas, text="Username:")
        self.user_select = ttk.Entry(self.main_canvas)

        self.input_password_label = tk.Label(self.main_canvas, text="Password:")
        self.input_password = tk.Entry(self.main_canvas, show="*", bg="white", fg="black")

        self.login_button = ttk.Button(self.main_canvas, text="Logon")

        self.input_ticket_label = tk.Label(self.main_canvas, text="Ticket Number:")
        self.input_ticket_number = tk.Entry(self.main_canvas, bg="white", fg="black")
        self.search_ticket_button = ttk.Button(self.main_canvas, text="Search Ticket")

        self.add_new_button = ttk.Button(self.main_canvas, text="Add New")
        self.log_out_button = ttk.Button(self.main_canvas, text="Log Out")
        self.edit_record_button = ttk.Button(self.main_canvas, text="Edit Ticket")
        self.save_update_button = ttk.Button(self.main_canvas, text="Save Edits")
        self.save_new_button = ttk.Button(self.main_canvas, text="Save New Ticket")

        self.user_select_label.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.user_select.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.input_password_label.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.input_password.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.login_button.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.log_out_button.grid(row=4, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.input_ticket_label.grid(row=5, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.input_ticket_number.grid(row=5, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.search_ticket_button.grid(row=6, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.edit_record_button.grid(row=7, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.save_update_button.grid(row=8, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.add_new_button.grid(row=9, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.save_new_button.grid(row=10, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.main_canvas.columnconfigure(0, minsize=100)
        self.main_canvas.columnconfigure(1, minsize=180)

    def create_form(self, master, ticket_number=None, ticket=None, datatypes=None, reference_table=None,
                    tasktypelink=None,
                    state=tk.DISABLED):

        column_index = 0
        row_index = 0
        _constraint_values = []
        constraint_values = []

        generic_canvas = tk.Canvas(master)
        self.generated_canvases["current_ticket"] = generic_canvas
        generic_canvas.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.user_inputs.clear()

        for key, value in ticket.items():
            label = tk.Label(generic_canvas, text=key, wraplength=100, justify='left', anchor='w')
            label.grid(row=row_index, column=column_index, sticky=tk.NW, rowspan=1)
            if key in reference_table.keys():
                for refkey, refvalue in reference_table.items():
                    if refkey == key:
                        for itemkey, item in refvalue.items():
                            _constraint_values.append(list(item))
                        for item in _constraint_values:  # This code right here is garbage, but its the only way I can eliminate the curly braces
                            constraint_values.append(item[0])
                        combobox = ttk.Combobox(generic_canvas, justify='left', width=50, values=constraint_values)
                        if value:
                            combobox.set(value)
                        combobox.grid(row=row_index, column=[column_index + 1], sticky=tk.NW, rowspan=1)
                        combobox.configure(state=state)
                        self.user_inputs[
                            key] = combobox  # To store user inputs as key value pair. This is used to get text from the widget when updating/creating new tickets
                        row_index += 1
                        _constraint_values.clear()
                        constraint_values.clear()
            elif key == "Notes":
                text = tk.Text(generic_canvas, height=10, width=40, wrap=tk.WORD)
                if value:
                    text.insert('1.0', value)
                text.grid(row=row_index, column=[column_index + 1], sticky=tk.NW, rowspan=1)
                text.configure(state=state)
                self.user_inputs[key] = text
                row_index += 1
            else:
                entry = tk.Entry(generic_canvas, justify='left', width=50)
                if value:
                    entry.insert(0, "{}".format(value))
                entry.grid(row=row_index, column=[column_index + 1], sticky=tk.NW, rowspan=1)
                entry.configure(state=state)
                self.user_inputs[
                    key] = entry  # To store user inputs as key value pair. This is used to get text from the widget when updating/creating new ticket
                row_index += 1

        # to initially configure the values within the 'tasktype' combobox
        # bind a function when there is a change to 'task' combobox
        # This is unfortunately hardcoded and a bit complicated
        task = self.user_inputs.get("Task")
        tasktype = self.user_inputs.get("Tasktype")
        tasktext = task.get()
        tasktype.configure(values=tasktypelink[tasktext])
        task.bind('<<ComboboxSelected>>',
                  lambda event, tasktypelink=tasktypelink: self.combobox_value_change(event,
                                                                                      tasktypelink))  # lambdas functions overly complicated

    def combobox_value_change(self, event, tasktypelink):
        task = self.user_inputs.get("Task")
        tasktype = self.user_inputs.get("Tasktype")
        tasktext = task.get()
        # print(tasktext)
        # print(tasktype.get())
        tasktype.delete(0, tk.END)
        # print(tasktype.get())
        # print(tasktypelink[tasktext])
        # print("four: ", tasktypelink)
        tasktype.configure(values=tasktypelink[tasktext])

    def create_table(self, master, fields=None, data=None, state=tk.DISABLED):
        column_index = 0
        row_index = 0

        generic_canvas = tk.Canvas(master)
        generic_canvas.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        for field in fields:
            label = tk.Label(generic_canvas,
                             text=field,
                             wraplength=100,
                             justify='left',
                             anchor='w')
            label.grid(row=row_index,
                       column=column_index,
                       sticky=tk.NW)
            column_index += 1
        row_index += 1
        column_index = 0

        for group in data:
            for item in group:
                entry = ttk.Entry(generic_canvas, justify='left')
                entry.insert(0, "{}".format(item))
                entry.grid(row=row_index,
                           column=column_index,
                           sticky=tk.NW)
                entry.configure(state=state)
                # self.user_inputs.append(entry)
                column_index += 1
            row_index += 1
            column_index = 0


###############CONTROLLER############################
class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.subscribe_to_observable()
        self.model.current_write_table(table_name='tblWTDWorkItems')
        self.initiate_application()

    # Subscriptions
    def subscribe_to_observable(self):
        self.model.myQuery.add_callback(call_id="call_IDIR", func=self.call_IDIR)
        self.model.myQuery.add_callback(call_id="call_user_tickets", func=self.call_user_tickets)

        self.model.myQuery.add_callback(call_id="call_ticket_number", func=self.call_ticket_number)
        self.model.myQuery.add_callback(call_id="call_current_record", func=self.call_current_record)
        self.model.myQuery.add_callback(call_id="call_current_write_table", func=self.call_current_write_table)
        self.model.myQuery.add_callback(call_id="call_current_tbl_datatypes", func=self.call_current_tbl_datatypes)
        self.model.myQuery.add_callback(call_id="call_ref_tasktypelink", func=self.call_ref_tasktypelink)
        self.model.myQuery.add_callback(call_id="call_write_ref_tblWTDWorkItems",
                                        func=self.call_write_ref_tblWTDWorkItems)
        # self.model.myQuery.add_callback(call_id="call_ref_table_workitem_constrains", func=self.call_ref_table_workitem_constrains)
        self.model.myQuery.add_callback(call_id="call_query_result", func=self.call_query_result)

    # application initiate/enable
    def initiate_application(self):
        self.view.login_button.configure(command=self.login)
        self.view.input_ticket_number.configure(state=tk.DISABLED)
        self.view.search_ticket_button.configure(state=tk.DISABLED, command=self.search_ticket)
        self.view.add_new_button.configure(state=tk.DISABLED, command=self.new_ticket)
        self.view.log_out_button.configure(state=tk.DISABLED, command=self.log_out)
        self.view.edit_record_button.configure(state=tk.DISABLED, command=self.edit_func)
        self.view.save_update_button.configure(state=tk.DISABLED, command=self.save_func)
        self.view.save_new_button.configure(state=tk.DISABLED, command=self.save_new_func)
        self.view.protocol("WM_DELETE_WINDOW", self.log_out)

    def enable_application(self):
        self.view.user_select.configure(state=tk.DISABLED)
        self.view.input_password.configure(state=tk.DISABLED)
        self.view.login_button.configure(state=tk.DISABLED)
        self.view.input_ticket_number.configure(state=tk.NORMAL)
        self.view.search_ticket_button.configure(state=tk.NORMAL)
        self.view.add_new_button.configure(state=tk.NORMAL)
        self.view.log_out_button.configure(state=tk.NORMAL)
        self.view.edit_record_button.configure(state=tk.NORMAL)
        # self.view.save_new_button.configure(state=tk.NORMAL)

    # View Button Functions
    def login(self, login_info=None):

        if not login_info:
            user = self.view.user_select.get()
            password = self.view.input_password.get()
            login_info = user, password

        try:
            _ = 1 / len(login_info[0])
            _ = 1 / len(login_info[1])
            self.model.validate_username(login_info)
        except ZeroDivisionError:
            msg.showerror("Login Failed", "Please enter Username or Password.")
        except IndexError:
            msg.showerror("Login Failed", "Invalid username/password combination.")
        else:
            self.model.load_user_tickets()
            self.enable_application()

    def search_ticket(self, ticket_number=None):
        if not ticket_number:
            ticket_number = self.view.input_ticket_number.get()
        try:
            _ = 1 / len(ticket_number)
            int(ticket_number)
            self.model.ticket_data(ticket_number=ticket_number)
        except ValueError:
            msg.showerror("Search Failed", "Ticket Number Must Be A Whole Number")
        except ZeroDivisionError:
            msg.showerror("Search Failed", "Please enter Ticket Number")

    def new_ticket(self):
        # new_ticket_template = self.model.myQuery.get(request="ticket_reference_write")
        self.model.write_template()
        for widget in self.view.user_inputs:
            self.view.user_inputs[widget].configure(state=tk.NORMAL)
        self.view.save_new_button.configure(state=tk.NORMAL)

    def edit_func(self):
        self.search_ticket()
        ticket_exists = self.model.myQuery.get(request="query_result")
        if ticket_exists:
            self.view.save_update_button.configure(state=tk.NORMAL)
            for widget in self.view.user_inputs:
                self.view.user_inputs[widget].configure(state=tk.NORMAL)

    def save_func(self):
        user_input = {}
        # current_record = self.model.myQuery.get(request="current_record")
        current_user = self.model.myQuery.get("IDIR")
        rev_reference_table = self.model.myQuery.get(request="rev_ref_table_workitem_constraints")
        print(rev_reference_table)
        self.view.save_update_button.configure(state=tk.DISABLED)
        user_input["LastEditedBy"] = current_user
        # print(current_record)
        # print(current_record.keys())

        for widgetkey, widgetvalue in self.view.user_inputs.items():
            if widgetkey in rev_reference_table.keys():
                for refkey, refvalue in rev_reference_table[widgetkey].items():
                    if refkey == widgetvalue.get():
                        widget_text = refvalue[0]
            elif widgetkey == "Notes":
                widget_text = self.view.user_inputs[widgetkey].get('1.0', 'end')
            else:
                widget_text = self.view.user_inputs[widgetkey].get()
            self.view.user_inputs[widgetkey].configure(state=tk.DISABLED)

            # print("COMPARE: ", widgetkey, widget_text, current_record[widgetkey])

            if widget_text == '':
                widget_text = None
            user_input[widgetkey] = widget_text

        print(user_input)
        self.model.update_ticket(user_input)

    def save_new_func(self):
        user_input = {}
        current_user = self.model.myQuery.get("IDIR")
        rev_write_ref_tblWTDWorkItems = self.model.myQuery.get(request="rev_write_ref_tblWTDWorkItems")
        print(rev_write_ref_tblWTDWorkItems)
        self.view.save_new_button.configure(state=tk.DISABLED)
        user_input["LastEditedBy"] = current_user

        for widgetkey, widgetvalue in self.view.user_inputs.items():
            if widgetkey in rev_write_ref_tblWTDWorkItems.keys():
                for refkey, refvalue in rev_write_ref_tblWTDWorkItems[widgetkey].items():
                    if refkey == widgetvalue.get():
                        widget_text = refvalue[0]
            elif widgetkey == "Notes":
                widget_text = self.view.user_inputs[widgetkey].get('1.0', 'end')
            else:
                widget_text = self.view.user_inputs[widgetkey].get()
            self.view.user_inputs[widgetkey].configure(state=tk.DISABLED)

            # print("COMPARE: ", widgetkey, widget_text, current_record[widgetkey])

            if widget_text == '':
                widget_text = None
            user_input[widgetkey] = widget_text

        print(user_input)
        new_ticket_number = self.model.add_ticket(user_input)
        self.search_ticket(str(new_ticket_number))

    def log_out(self):
        if msg.askokcancel("Log Out", "Do you really want to exit?"):
            self.view.destroy()

    # Other Support Functions
    def refresh_view_data(self, identifier):
        try:
            self.view.generated_canvases[identifier].destroy()
            del self.view.generated_canvases[identifier]
        except KeyError:
            print('KEYVALUE EXCEPTION')

        #     self.view.ticket_canvas_widget[0].destroy()
        #     self.view.ticket_canvas_widget.clear()

    # Callbacks
    def call_IDIR(self):
        IDIR = self.model.myQuery.get(request="IDIR")
        self.view.title("{} has entered the Batcave".format(IDIR))

    def call_ticket_number(self):
        pass

    def call_user_tickets(self, state=tk.DISABLED):
        user_tickets = self.model.myQuery.get(request="USER_TICKETS")
        ticket_headers = user_tickets[0]
        ticket_records = user_tickets[1]
        self.view.create_table(master=self.view.zone_2,
                               fields=ticket_headers,
                               data=ticket_records,
                               state=state)

    def call_current_record(
            self):  # I should now be able to call this function for edit and just change the state for the edit function
        current_record = self.model.myQuery.get(request="current_record")
        current_tbl_datatypes = self.model.myQuery.get(request="current_tbl_datatypes")
        write_ref_tblWTDWorkItems = self.model.myQuery.get(request="write_ref_tblWTDWorkItems")
        ref_tasktypelink = self.model.myQuery.get(request="ref_tasktypelink")
        ticket_number = self.model.myQuery.get(request="ticket_number")
        # print("one: ", ref_tasktypelink)
        self.refresh_view_data(identifier="current_ticket")
        self.view.create_form(master=self.view.zone_3,
                              ticket_number=ticket_number,
                              ticket=current_record,
                              datatypes=current_tbl_datatypes,
                              reference_table=write_ref_tblWTDWorkItems,
                              tasktypelink=ref_tasktypelink)
        # print(self.view.generated_canvases.items())

    def call_query_result(self):
        query_result = self.model.myQuery.get(request="query_result")
        if not query_result:
            msg.showerror("Search Failed", "Cannot find BATMAN Ticket")

    def call_current_write_table(self):
        pass

    def call_current_tbl_datatypes(self):
        pass

    def call_ref_tasktypelink(self):
        pass

    def call_write_ref_tblWTDWorkItems(self):
        pass


if __name__ == "__main__":
    BATCAVE = Controller()
    BATCAVE.view.mainloop()
