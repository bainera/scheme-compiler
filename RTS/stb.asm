STRING_TO_SYMBOL_BODY:
                        PUSH(FP);
                        MOV(FP,SP);
                        PUSH(R1);
                        PUSH(R2);
                        PUSH(R9);
                        PUSH(R12);
                        PUSH(R10);
                        MOV(R1,FPARG(2)); // holds the ADRESS OF "given-string"
                        MOV(R0,IMM(7));
MOV (R9,R0); // SAVE THE ADRESS OF FIRST BUCKET

                        COMPARING_STRINGS:
                        CMP (R1,R0);     //COMPARE THE GIVEN _STRING WITH THE T_STRING AT THE FISRT CELL OF THE CHECKED BUCKET
                        JUMP_LT (SEARCH_IN_CONSTANTS_TABLE);
                        JUMP_NE(CHECK_NEXT_BUCKET);

                        //CREAT A NEW SYMBOL
                        PUSH (R0);
                        CALL(MAKE_SOB_SYMBOL);
                        DROP(1);
                        JUMP(FOUND);

                        CHECK_NEXT_BUCKET:
                        MOV(R0,INDD(R0,2)); //update R0 to point the adress of the next bucket
                        JUMP(COMPARING_STRINGS);

                        SEARCH_IN_CONSTANTS_TABLE:

                        MOV(R10,INDD(R1,1));   //GET THE NUM_OF_CHARS FROM THE GIVEN T_STRING
                        ADD(R10,2);     // ELTA TO NEXT CELL AFTER T_STRING/
                        ADD(R10,R1);      //KEPP IN R1 THE OPTINAL SYMBOL
                        MOV(R0,R10);
                        CMP (R10,T_SYMBOL);
                        JUMP_EQ(FOUND);

                        //CREATE A NEW SYMBOL POINTING TO A NEW BUCKET HOLDING IN THE FIRST CELL THE GIVEN T_STRING

                        PUSH(IMM(3));
                        CALL(MALLOC);
                        DROP(1);
                        MOV(R12,R0); //KEPP THE ADRESS OF THE CREATED BUCKET
                        MOV (INDD(R12,2),IMM(0)); //UPDATED PONITER TO THE NEXT BUCKET (ZERO)
                        MOV (INDD(R12,1),IMM(777)); //UPDATE FICTIVE VALUE
                        MOV (IND(R12),R1); //UPDATE THE T_STRING OF THE BUCKET
                        PUSH(R12);
                        CALL(MAKE_SOB_SYMBOL);
                        DROP(1);

                        FOUND:
                        POP(R10);
                        POP(R12);
                        POP(R9);
                        POP(R2);
                        POP(R1);
                        POP(FP);
                        RETURN;
                        