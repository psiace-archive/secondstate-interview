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

