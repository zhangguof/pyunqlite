#-*- coding:utf-8 -*-

import sys
sys.path.append("pyunqlite/Release")

import _unqlite

#const
UNQLITE_OPEN_READONLY       = 0x00000001  #/* Read only mode. Ok for [unqlite_open] */
UNQLITE_OPEN_READWRITE      = 0x00000002  #/* Ok for [unqlite_open] */
UNQLITE_OPEN_CREATE         = 0x00000004  #/* Ok for [unqlite_open] */
UNQLITE_OPEN_EXCLUSIVE      = 0x00000008  #/* VFS only */
UNQLITE_OPEN_TEMP_DB        = 0x00000010  #/* VFS only */
UNQLITE_OPEN_NOMUTEX        = 0x00000020  #/* Ok for [unqlite_open] */ UNQLITE_OPEN_OMIT_JOURNALING  0x00000040  /* Omit journaling for this database. Ok for [unqlite_open] */
UNQLITE_OPEN_IN_MEMORY      = 0x00000080  #/* An in memory database. Ok for [unqlite_open]*/
UNQLITE_OPEN_MMAP           = 0x00000100  #/* Obtain a memory view of the whole file. Ok for [unqlite_open] /




if __name__ == "__main__":
    jx9_prog="/* Create the collection 'users'  */"\
 "if( !db_exists('users') ){"\
 "   /* Try to create it */"\
 "  $rc = db_create('users');"\
 "  if ( !$rc ){"\
 "    /*Handle error*/"\
 "    print db_errlog();"\
 "	  return;"\
 "  }else{"\
 "     print \"Collection 'users' successfuly created\\n\";"\
 "   }"\
 " }"\
 "/*The following is the records to be stored shortly in our collection*/ "\
 "$zRec = ["\
 "{"\
 "  name : 'james',"\
 "  age  : 27,"\
 "  mail : 'dude@example.com'"\
 "},"\
 "{"\
 "  name : 'robert',"\
 "  age  : 35,"\
 "  mail : 'rob@example.com'"\
 "},"\
 "{"\
 "  name : 'monji',"\
 "  age  : 47,"\
 "  mail : 'monji@example.com'"\
 "},"\
 "{"\
 " name : 'barzini',"\
 " age  : 52,"\
 " mail : 'barz@mobster.com'"\
 "}"\
 "];"\
 "/*Store our records*/"\
 "$rc = db_store('users',$zRec);"\
 "if( !$rc ){"\
 " /*Handle error*/"\
 " print db_errlog();"\
 " return;"\
 "}"\
 "/*Create our filter callback*/"\
 "$zCallback = function($rec){"\
 "   /*Allow only users >= 30 years old.*/"\
 "   if( $rec.age < 30 ){"\
 "       /* Discard this record*/"\
 "       return FALSE;"\
 "   }"\
 "   /* Record correspond to our criteria*/"\
 "   return TRUE;"\
 "}; /* Don't forget the semi-colon here*/"\
 "/* Retrieve collection records and apply our filter callback*/"\
 "$data = db_fetch_all('users',$zCallback);"\
 "print \"Filtered records\\n\";"\
 "/*Iterate over the extracted elements*/"\
 "foreach($data as $value){ /*JSON array holding the filtered records*/"\
 " print $value..JX9_EOL;"\
 "}"
    handle = _unqlite.unqlite_open(":mem:",UNQLITE_OPEN_CREATE)
    _unqlite.unqlite_compile(handle,jx9_prog,len(jx9_prog))