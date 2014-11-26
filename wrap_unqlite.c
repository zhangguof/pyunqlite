#include "Python.h"
#include "unqlite.h"



static void Fatal(unqlite *pDb,const char *zMsg)
{
	if( pDb ){
		const char *zErr;
		int iLen = 0; /* Stupid cc warning */

		/* Extract the database error log */
		unqlite_config(pDb,UNQLITE_CONFIG_ERR_LOG,&zErr,&iLen);
		if( iLen > 0 ){
			/* Output the DB error log */
			puts(zErr); /* Always null termniated */
		}
	}else{
		if( zMsg ){
			puts(zMsg);
		}
	}
	/* Manually shutdown the library */
	unqlite_lib_shutdown();
	/* Exit immediately */
	exit(0);
}


static PyObject*
wrap_unqlite_open(PyObject* self, PyObject *args)
{
	const char *zFilename;
	unsigned int iMode;

	struct unqlite *pDb;
	struct unqlite_vm *pVm;
	int rc;

	if (!PyArg_ParseTuple(args,"sl",&zFilename,&iMode))
		return NULL;


	rc = unqlite_open(&pDb,zFilename,iMode);
	if( rc != UNQLITE_OK ){
		Fatal(0,"Out of memory");
		return Py_None;
	}
	return Py_BuildValue("l",pDb);
}
static PyObject*
wrap_unqlite_compile(PyObject *self, PyObject *args)
{
	int rc;
	struct unqlite_vm *pVm;
	
	struct unqlite *pDb;
	const char* jx9_prog;
	int prog_len;
	if (!PyArg_ParseTuple(args,"lsl",&pDb,&jx9_prog,&prog_len))
		return NULL;

	rc = unqlite_compile(pDb,jx9_prog,prog_len,&pVm);

	if( rc != UNQLITE_OK ){
		/* Compile error, extract the compiler error log */
		const char *zBuf;
		int iLen;
		/* Extract error log */
		unqlite_config(pDb,UNQLITE_CONFIG_JX9_ERR_LOG,&zBuf,&iLen);
		if( iLen > 0 ){
			puts(zBuf);
		}
		Fatal(0,"Jx9 compile error");
	}
	//printf("unqlite compile ok.\n");


	/* Install a VM output consumer callback */
	//rc = unqlite_vm_config(pVm,UNQLITE_VM_CONFIG_OUTPUT,VmOutputConsumer,0);
	//if( rc != UNQLITE_OK ){
	//	Fatal(pDb,0);
	//}

	/* Execute our script */
	rc = unqlite_vm_exec(pVm);
	if( rc != UNQLITE_OK ){
		Fatal(pDb,0);
	}

	/* Release our VM */
	unqlite_vm_release(pVm);

	/* Auto-commit the transaction and close our database */
	//unqlite_close(pDb);
	return Py_None;

}


static PyObject *
ex_foo(PyObject *self, PyObject *args)
{
	printf("Hello, world\n");
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef _unqlite_methods[] = {
	{"foo", ex_foo, METH_VARARGS, "foo() doc string"},
	{"unqlite_open",wrap_unqlite_open,METH_VARARGS,"unqlite open."},
	{"unqlite_compile",wrap_unqlite_compile,METH_VARARGS,"unqlite compile."},
	{NULL, NULL}
};

PyMODINIT_FUNC
init_unqlite(void)
{
	Py_InitModule("_unqlite", _unqlite_methods);
}

