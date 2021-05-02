//
//  File.swift
//  Notes
//
//  Created by MaC on 29/11/2020.
//

import Foundation
import SQLite3
struct Note {
    let id: Int
    var contents: String
}

class NoteManager {
    var database: OpaquePointer!
    static let main = NoteManager()
    private init(){
    }
    func connect(){
        if database != nil {
            return
        }
        do {
            let databaseURL = try FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true).appendingPathComponent("note.sqlite3")
            if sqlite3_open(databaseURL.path, &database) == SQLITE_OK{
                if sqlite3_exec(database, "CREATE TABLE IF NOT EXISTS notes (contents TEXT)", nil, nil, nil) == SQLITE_OK{
                    
                }
                else {
                    print("Could not create table")
                }
                
            }
            else{
                print("Could not connect")
            }
            }
        
        catch let error {
            print("Could not create database")
        }
    }
    func create() -> Int {
        connect()
        var statement: OpaquePointer? = nil
        if sqlite3_prepare_v2(database, "INSERT INTO notes (contents) VALUES ('New note')", -1, &statement, nil) != SQLITE_OK {
            print("Could not create query")
            return -1
        }
            if sqlite3_step(statement) != SQLITE_DONE{
                print("Could not insert note")
                return -1
            }

        sqlite3_finalize(statement)
        return Int(sqlite3_last_insert_rowid(database))
    }
    
    func getAllNotes() -> [Note]{
        connect()
        var result: [Note] = []
        var statement: OpaquePointer? = nil 
        if sqlite3_prepare_v2(database, "SELECT rowid, contents FROM notes", -1, &statement, nil) != SQLITE_OK{
            print("Error creating select")
            return []
        }
        while sqlite3_step(statement) == SQLITE_ROW{
            result.append(Note(id: Int(sqlite3_column_int(statement, 0)), contents: String(cString: sqlite3_column_text(statement, 1))))
        }
        sqlite3_finalize(statement)
        return result
    }
    func save (note: Note) {
        connect()
        var statement: OpaquePointer? = nil
        if sqlite3_prepare(database, "UPDATE notes SET contents = ? WHERE rowid = ?", -1, &statement, nil) != SQLITE_OK{
            print("Error creating update statement")
        }
        sqlite3_bind_text(statement, 1, NSString(string: note.contents).utf8String, -1, nil)
        sqlite3_bind_int(statement, 2, Int32(note.id))
        if sqlite3_step(statement) != SQLITE_DONE{
            print("Error running update")
        }
        sqlite3_finalize(statement)
    }
    func delete (RowToDelete: Int32){
        connect()
        var statement: OpaquePointer? = nil
        if sqlite3_prepare(database, "DELETE FROM notes WHERE rowid = ?", -1, &statement, nil) != SQLITE_OK{
            print("Unable to delete a row")
        }
        sqlite3_bind_int(statement, 1, Int32(RowToDelete))

        if sqlite3_step(statement) != SQLITE_DONE{
            print("Error running delete")
        }
        sqlite3_finalize(statement)
    }
    
}




