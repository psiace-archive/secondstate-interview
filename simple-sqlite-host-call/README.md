# Example
1. Host function allocation
    Developers can define C functions with the following function signature as the host function body:

    ```c
    typedef WasmEdge_Result (*WasmEdge_HostFunc_t)(
      void *Data,
      WasmEdge_MemoryInstanceContext *MemCxt,
      const WasmEdge_Value *Params,
      WasmEdge_Value *Returns);
    ```
    The example of an `Visit_Sqlite` host function to call the SQLite:

    ```c
	WasmEdge_Result Visit_Sqlite(void *Data, WasmEdge_MemoryInstanceContext *MemCxt,
		            const WasmEdge_Value *In, WasmEdge_Value *Out) {
		static sqlite3 * db=NULL;
		static char * errmsg=NULL;
		static char ** Result=NULL;
		
		int32_t Val1 = WasmEdge_ValueGetI32(In[0]);
		
		int32_t rc,nrow,ncolumn;
		if(Val1)
		{
			rc=sqlite3_open("test.db",&db);
		}
		
	  	Out[0] = WasmEdge_ValueGenI32(0);
		if(rc)
		{
			printf("can't open database!\n");
		}
		else
		{
			printf("open database success!\n");
			rc=sqlite3_get_table(db,"select * from test_table",&Result,&nrow,&ncolumn,&errmsg);
			if(!rc)
			{  
				for(int32_t i=1;i<nrow;i++)
				{  
					for(int32_t j=0;j<ncolumn;j++)
					{  
						printf("%s|",Result[i*ncolumn+j]);
					}  
					printf("\n");
				}
				Out[0] = WasmEdge_ValueGenI32(1);
			}
		}
		sqlite3_close(db);	

		return WasmEdge_Result_Success;
	}
    ```

2. Import object context

    The `Import Object` context holds an exporting module name and the instances. Developers can add the `Host Function`, `Memory`, `Table`, and `Global` instances with their exporting names.

    ```c
    /* Create the import object. */
    WasmEdge_String ExportName = WasmEdge_StringCreateByCString("module");
    WasmEdge_ImportObjectContext *ImpObj = WasmEdge_ImportObjectCreate(ExportName);
    WasmEdge_StringDelete(ExportName);

    /* Create and add a host function instance into the import object. */
    enum WasmEdge_ValType ParamList[1] = { WasmEdge_ValType_I32 };
    enum WasmEdge_ValType ReturnList[1] = { WasmEdge_ValType_I32 };
    WasmEdge_FunctionTypeContext *HostFType = 
      WasmEdge_FunctionTypeCreate(ParamList, 1, ReturnList, 1);
    WasmEdge_HostFunctionContext *HostFunc =
      WasmEdge_HostFunctionCreate(HostFType, Visit_Sqlite, NULL, 0);
    /*
     * The third parameter is the pointer to the additional data object.
     * Developers should guarantee the life cycle of the data, and it can be
     * `NULL` if the external data is not needed.
     */
    WasmEdge_FunctionTypeDelete(HostFType);
    WasmEdge_String FuncName = WasmEdge_StringCreateByCString("func-sqlite");
    WasmEdge_ImportObjectAddHostFunction(ImpObj, FuncName, HostFunc);
    WasmEdge_StringDelete(FuncName);

    /*
     * Developers should destroy the import object context if it is not registered into a
     * store context or a VM context.
     * Developers should __NOT__ destroy the instances added into the import object contexts.
     */
    WasmEdge_ImportObjectDelete(ImpObj);
    ```

3. Example

    The `sqlite_host.wat` is a handwritten WebAssembly script to calls this host function. It is compiled into WebAssembly using the [WABT tool](https://github.com/WebAssembly/wabt).
    The bash to compile `sqlite_host.wat` to `sqlite_host.wasm` as following:
    ```bash
    wat2wasm sqlite_host.wat -o sqlite_host.wasm
    
    ```
    
    The simple WASM from the WAT as following:

    ```
    (module
      (type $t0 (func (param i32) (result i32)))
      (import "extern" "func-sqlite" (func $f-sqlite (type $t0)))
      (func (export "visit_sqlite") (param i32) (result i32)
        local.get 0
        call $f-sqlite)
    )
    ```

    And the `sqlite_host.c` as following:

    ```c
	#include <wasmedge/wasmedge.h>
	#include <stdio.h>
	#include <sqlite3.h>

	/* Host function body definition. */
	WasmEdge_Result Visit_Sqlite(void *Data, WasmEdge_MemoryInstanceContext *MemCxt,
		            const WasmEdge_Value *In, WasmEdge_Value *Out) {
		static sqlite3 * db=NULL;
		static char * errmsg=NULL;
		static char ** Result=NULL;
		
		int32_t Val1 = WasmEdge_ValueGetI32(In[0]);
		
		int32_t rc,nrow,ncolumn;
		if(Val1)
		{
			rc=sqlite3_open("test.db",&db);
		}
		
	  	Out[0] = WasmEdge_ValueGenI32(0);
		if(rc)
		{
			printf("can't open database!\n");
		}
		else
		{
			printf("open database success!\n");
			rc=sqlite3_get_table(db,"select * from test_table",&Result,&nrow,&ncolumn,&errmsg);
			if(!rc)
			{  
				for(int32_t i=1;i<nrow;i++)
				{  
					for(int32_t j=0;j<ncolumn;j++)
					{  
						printf("%s|",Result[i*ncolumn+j]);
					}  
					printf("\n");
				}
				Out[0] = WasmEdge_ValueGenI32(1);
			}
		}
		sqlite3_close(db);	

		return WasmEdge_Result_Success;
	}

	int main(int Argc, const char* Argv[]) {
		/* Create the VM context. */
		WasmEdge_VMContext *VMCxt = WasmEdge_VMCreate(NULL, NULL);

		/* Create the import object. */
		WasmEdge_String ExportName = WasmEdge_StringCreateByCString("extern");
		WasmEdge_ImportObjectContext *ImpObj = WasmEdge_ImportObjectCreate(ExportName);
		enum WasmEdge_ValType ParamList[1] = { WasmEdge_ValType_I32 };
		enum WasmEdge_ValType ReturnList[1] = { WasmEdge_ValType_I32 };
		WasmEdge_FunctionTypeContext *HostFType = WasmEdge_FunctionTypeCreate(ParamList, 1, ReturnList, 1);
		WasmEdge_HostFunctionContext *HostFunc = WasmEdge_HostFunctionCreate(HostFType, Visit_Sqlite, NULL, 0);
		WasmEdge_FunctionTypeDelete(HostFType);
		WasmEdge_String HostFuncName = WasmEdge_StringCreateByCString("func-sqlite");
		WasmEdge_ImportObjectAddHostFunction(ImpObj, HostFuncName, HostFunc);
		WasmEdge_StringDelete(HostFuncName);

		WasmEdge_VMRegisterModuleFromImport(VMCxt, ImpObj);

		/* The parameters and returns arrays. */
		WasmEdge_Value Params[1] = { WasmEdge_ValueGenI32(1) };
		WasmEdge_Value Returns[1];
		/* Function name. */
		WasmEdge_String FuncName = WasmEdge_StringCreateByCString("visit_sqlite");
		/* Run the WASM function from file. */
		WasmEdge_Result Res = WasmEdge_VMRunWasmFromFile(
			VMCxt, "sqlite_host.wasm", FuncName, Params, 1, Returns, 1);

		if (WasmEdge_ResultOK(Res)) {
			if(WasmEdge_ValueGetI32(Returns[0])==1) printf("Get the data successfully!\n");
		} 
		else {
			printf("Error message: %s\n", WasmEdge_ResultGetMessage(Res));
		}

		/* Resources deallocations. */
		WasmEdge_VMDelete(VMCxt);
		WasmEdge_StringDelete(FuncName);
		WasmEdge_ImportObjectDelete(ImpObj);
		return 0;
	}
    ```

    Then you can compile and run: 

    ```bash
    $ gcc sqlite_host.c -lwasmedge_c -lsqlite3 -o sqlite_host.out
    $ ./sqlite_host.out
    open database success!
    wanghu|male|24|
    wanghu|male|24|
    Get the data successfully!

    ```

