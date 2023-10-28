class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    #takes in no parameters 
    #checks if the stack is empty
    #returns True if empty and false if not 
    def isEmpty(self):
        if self.top is None:
            return True
        else:
            return False

    #takes in no parameters 
    #checks how many items in stack 
    #returns the numnber of items
    def __len__(self): 
        current=self.top
        count=0
        while current is not None:
            count+=1
            current=current.next
        return count
        
    #takes in an item
    #makes a new node and adds the node to the top of the stack
    #returns None
    def push(self,value):
        newNode=Node(value)
        if self.top is None:
            self.top=newNode
        else:
            newNode.next=self.top
            self.top=newNode

    #takes in no parameters
    #removes the top node of the stack
    #returns the value of the removed node and None if stack is empty
    def pop(self):
        current=self.top
        if self.isEmpty():
            return None
        else:
            self.top=self.top.next
            current.next=None
            return current.value

    #takes in no paramters 
    #checks the value of the node on top of the stack
    #returns the value of the top node and None if stack is empty
    def peek(self):
        current=self.top
        if self.isEmpty():
            return None
        else:
            return current.value

#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None
    
    #takes in a string (could be an integer/float or mix of integers/float and characters)
    #checks if the characters of the string are all integers and turns valid strings into floats
    #returns True if integer/float and false otherwise 
    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        try:
            float(txt)
            return True
        except ValueError:
            return False

            

    #watch the lectures!
    #separate txt into a list of tokens (there's more logic than just calling strings's split method)
    #validate txt and/or the list of tokens to make sure:
    #       parantheses are balanced
    #       no numbers are next to each other
    #       no operators are next to each other (but "3 - -5" is ok)
    #       one way to check is to loop and keep counts of parantheses and numbers/operators. For example, "(" -> +1, ")" -> -1 and the count should end at 0
    #Use a dictionary to store operator precedence (can use "^" as highest, "(" as lowest)
    #   Loop through tokens
    #       numbers get added to the postFix
    #       ( and ^ are added to the stack 
    #       ) pops until (
    #       * / + - pop until they find an operator of a lower priority
    
    #takes in a parameter(string)
    #converts an expression from infix to postfix and all numbers are represented as floats
    #returns a string of the expression in postfix form and None if expression is invalid
    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('     2 ^       4')
            '2.0 4.0 ^'
            >>> x._getPostfix('          2 ')
            '2.0'
            >>> x._getPostfix('2.1        * 5        + 3       ^ 2 +         1 +             4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2*5.34+3^2+1+4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( .5 )')
            '0.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('((2 *((5 + 3  ) ^ 2 + (1 +4 ))    ))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2* (       -5 + 3 ) ^2+ ( 1 +4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('     2 * 5 + 3  ^ * 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5      + 3 ) ^ 2 + ( 1 +4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^  2 + ) 1 + 4 (')
            >>> x._getPostfix('2 *      5% + 3       ^ + -2 +1 +4')
        '''
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        output=[]
        opr="+-*/^()"
        oprno_m="+*/^"
        oprnopar='+-*/^'
        oprprior={'(': 1, '+': 2 ,'-': 2, '*': 3, '/':3, '^': 4}
        lst=[]
        temp_num=''
        for char in range(len(txt)):
            if txt[char] != " ":
               lst.append(txt[char])
            elif self._isNumber(txt[char]) or txt[char] != " ":
                temp_num+=txt[char]
            elif txt[char]=='.' or txt[char] != " ":
                temp_num+=txt[char]
            elif txt[char] in opr:
                lst.append(temp_num)
                lst.append(txt[char])
                temp_num=''
            #lst.append(temp_num)
            #print(lst)
            

        
        '''
        ###old check for decimal
        for char in txt:
            temp_num=''
            if self._isNumber(char):
                while char!=' ' or char!=opr:
                    temp_num+=char
                lst.append(temp_num)
            if char != " ":
                lst.append(char)
        print(lst)
        '''

        '''
        countopr_num=0
        for i in lst:
            if self._isNumber(i):
                countopr_num+1
            elif i in oprnopar:
                countopr_num-=1
            if countopr_num!=1:
                return None
        
        temp=''
        for i in range(len(lst)):
            if not self._isNumber(lst[i]) or lst[i] not in opr:
                return None
            if lst[i]=='-':
                if self._isNumber(lst[i-1]):
                    postfixStack.push(lst[i])
                elif lst[-1]=='-' and self._isNumber(lst[i+1]):
                    temp+=lst[i]+lst[i+1]
                    output+=[temp]
                else:
                    postfixStack.push(lst[i])
            elif self._isNumber(lst[i]) and lst[i+1]=='(':
                return None
            elif lst[i] in oprnopar and lst[i+1] in oprno_m:
                return None
            else:
                return None
        '''
        countpar=0
        for token in lst:
            if self._isNumber(token):
                numtxt=str(float(token))
                output+=[numtxt]
            elif token=='(':
                countpar+=1
                postfixStack.push(token)
            elif token==')':
                countpar-=1
                while postfixStack.peek()!='(' and not postfixStack.isEmpty():
                    if countpar==0:
                        pop1=postfixStack.pop()
                        output+=pop1
                    else:
                        return None
                postfixStack.pop()
            elif token in oprprior:
                while not postfixStack.isEmpty() and oprprior[token]<=oprprior[postfixStack.peek()]:
                    pop=postfixStack.pop()
                    output+=pop
                postfixStack.push(token)
            else:
                return None

        while not postfixStack.isEmpty():
            pop=postfixStack.pop()
            output+=pop
        outputstr=" ".join(output)
        return outputstr

    #takes in no paramters
    #uses self.__expr and translate it to postfix using _getPostfix, then the numbers and operators in the expression are used to calculate a final value
    #returns the result of expression and None if invalid computation of expression
    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            
            >>> x=Calculator()
            >>> x.setExpr('4        + 3 -       2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 +          3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('      4 +           3.65  - 2        / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25      * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr('2-3*4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ((( 10 - 2*3 )) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('      8 / 4 * (3 - 2.45 * ( 4   - 2 ^ 3 )       ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 +        2 * (         5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            >>> x.calculate
            1442.7777777777778
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 ++ 3+ 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 +2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 *( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( *10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            >>> x.setExpr('(    3.5 ) ( 15 )') 
            >>> x.calculate
            >>> x.setExpr('3 ( 5) - 15 + 85 ( 12)') 
            >>> x.calculate
            >>> x.setExpr("( -2/6) + ( 5 ( ( 9.4 )))") 
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the  expression

        getpostfix=self._getPostfix(self.__expr)
        if getpostfix==None:
            return None

        lst=getpostfix.split()
        for i in lst:
            if self._isNumber(i):
                calcStack.push(float(i))
            else:
                pop1=calcStack.pop()
                pop2=calcStack.pop()
                if i=='^':
                    evaluate=pop2**pop1
                    calcStack.push(evaluate)
                elif i=='*':
                    evaluate=pop2 * pop1
                    calcStack.push(evaluate)
                elif i=='/' and pop1!=0: # check for division by zero
                    evaluate=pop2 / pop1
                    calcStack.push(evaluate)
                elif i=='+':
                    evaluate=pop2 + pop1
                    calcStack.push(evaluate)
                elif i=='-':
                    evaluate=pop2 + pop1
                    calcStack.push(evaluate)
                else:
                    return None
        if calcStack.__len__()==1:
            result=calcStack.pop() 
            return result
        else:
            return None          

#=============================================== Part III ==============================================

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}
    
    #takes in a string 
    #checks if the string is a valid variable. Valid if: not empty, first character is letter, characters are alphanumeric 
    #returns True if valid and False otherwise 
    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        if isinstance(word,str):
            if word[0].isalpha() and word.isalnum():
                return True
            else:
                return False
        else:
            return False
       
    #takes in a string 
    #if there are variables in string that are in self.states, then they are replaced by the value of the key 
    #returns a valid expression and None if variables not in self.states
    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        opr="+-*/^()"
        lst=expr.split()
        newlst=[]
        for char in lst:
            if self._isVariable(char) and char not in self.states:
                return None
            elif char in self.states:
                x=self.states[char]
                newlst.append(str(x))
            elif char in opr:
                newlst.append(char)
            elif isinstance(float(char),float):
                newlst.append(str(char))
            else:
                return None
        newexpr=" ".join(newlst)
        return newexpr



    #calculateExpressions() must use the Calculator object provided in the starter code
    #split the expression to separate out lines and variable names 
    #all of your logic should just prepare the expression to be calculated, you use calcobj to do the actual math
    #the states dictionary is a snapshot of all the variable values, not only the value you just calculated
    #   dictionary.copy() can be useful for getting an identical dictionary while preserving the old dictionary

    #takes in no parameters
    #evaluates expression in self.expressions and each valid varialble is replaced with their values, and the Calculator object is used to calculate the expression.
    #continue... dictionary self.states us updated based on the process of the calculation of the expression where the key in the line evaluated and value the current state of self.states after the line is evaluated. The dictionary ends with key: __return__ and value being returned
    #returns dictionary of the all the states of self.states as calculation progresses, otherwise None
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        nwd=self.states.copy
        eval=self._replaceVariables(self.expressions)
        if eval==None:
            return None
        lst=eval.split()

if __name__=='__main__':
    import doctest
    #doctest.testmod()  # OR
    doctest.run_docstring_examples(Calculator._getPostfix, globals(), name='LAB2',verbose=True) # replace Pantry with the class name you want to test