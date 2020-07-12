from django import template
from django.template.defaultfilters import stringfilter

import re
import io

register = template.Library()
# pre inside a li 


@register.filter()
@stringfilter




   
def markdown_parser(markdown):
    results=''
    ultag_is_open = False
    sub_ultag_is_open =False    
    ol_is_open =False
    previouslinespace = 0
    count =0
    
    for line in markdown.splitlines():
        
        #previouslinespace = len(line)-len(line.lstrip())
        #heading    
        heading = re.compile("#+\s") 
        heading_matches = heading.search(line.strip())
        
        
        #list
        
        #li = re.compile(r"(\-\s|\*\s)([\w+(\[|\^&+\-.',%\(\/)=!\:>\'\"\s]+?)(?<=$)",re.MULTILINE)

        #li =re.compile(r"^((\-\s|\*\s)([\w+(\[|\^&+\-.',%\(\/)=!\:>\'\"\s]+?)(?<=\n))",re.MULTILINE)

        #working pattern
        #if ifultag==False:
        

        ordered_list = re.compile(r"^\s*(\d+\.\s*)(.+?)(?<=$)")
        if ordered_list.search(line):
            if ol_is_open == False: 
                line = ordered_list.sub(r"<ol><li>\2</li>",line)
                ol_is_open =True
            else:
                line = ordered_list.sub(r"<li>\2</li>",line)
        else:
            if ol_is_open ==True:
                line ="</ol>"+'\n'+line
                oltag_is_open =False


        unordered_list = re.compile(r"^\s*(\-\s|\*\s)([\w+(\[|\^&+\-.',%\(\/)=!\:>\'\"\*\s]+?)(?<=$)",re.MULTILINE)
        print("line",line)
        if unordered_list.search(line):
            #nested li is defined in such a way that difference between 
            # new li and prev li must be diff>=2 and diff<=5 spaces
            print ('LIST exists')
            currentlinespace = len(line)-len(line.lstrip())
            print("Current Line's Space",currentlinespace)
            print("Previous line space",previouslinespace)
            
            #handling non nested li
            #if previouslinespace == 0: #new list
            if currentlinespace-previouslinespace== 0: 
                print("HERE 1")
                #new line is not a nested li
                if ultag_is_open == True: #not a first li in the list
                    print("HERE 1 only LI")
                    line = unordered_list.sub(r"<li>\2</li>",line) #add  li tag
                else:
                    #first li in the list
                    print("HERE 1 only UL")
                    line = unordered_list.sub(r"<ul>\n<li>\2</li>",line)
                    ultag_is_open = True #set ul tag to open
                previouslinespace = currentlinespace

            
            elif 2<=currentlinespace-previouslinespace<=5:
                print("HERE 2")
                if ultag_is_open == True: #not a first li in the list
                    if sub_ultag_is_open :
                        print("HERE 2 only LI")
                        print("count",count)
                        if count>=1:
                            line = unordered_list.sub(r"<ul><li>\2</li>\n",line) #add  li tag
                        line = unordered_list.sub(r"<li>\2</li>\n",line) #add  li tag
                    else:
                        print("HERE 2 UL")
                        #firstline_space = previouslinespace
                        sub_ultag_is_open = True
                        count +=1
                        line = unordered_list.sub(r"<ul>\n<li>\2</li>\n",line)
                else:
                    #first li in the list
                    print("HERE 2 only UL")
                    line = unordered_list.sub(r"<ul>\n<li>\2</li>\n",line)
                    ultag_is_open = True #set ul tag to open
                previouslinespace = currentlinespace

            #currentlinespace<previouslinespace:
            else: #currentlinespace<previouslinespace
                print("if ul is open?",ultag_is_open)
                
                if ultag_is_open == True:
                    
                    line ="</ul>"+'\n'+line
                    ultag_is_open = False
                if  sub_ultag_is_open ==True:
                    line ="</ul>"+'\n'+line
                    sub_ultag_is_open =False
                print("Number of ul tag to be closed" ,count)
                if count >=1:
                    for i in range(count):
                        ultags ="</ul>"+'\n'
                    line =ultags +line
                    count =0     
                print("Line before substitution",line) 
                line = unordered_list.sub(r"<ul>\n<li>\2</li>",line)
                ultag_is_open = True #set ul tag to open
                previouslinespace = currentlinespace
                print("Line after substitution",line) 
                         


            # else:
            #     if previouslinespace == 0: #new list
            #         print("HERE 3")
            #         if ultag_is_open == True: #not a first li in the list
            #             print("HERE 3 only LI")
            #             line = unordered_list.sub(r"<li>\2</li>\n",line) #add  li tag
            #         else:
            #             #first li in the list
            #             print("HERE 3 only UL")
            #             line = unordered_list.sub(r"<ul>\n<li>\2</li>\n",line)
            #             ultag_is_open = True #set ul tag to open
            #         previouslinespace = currentlinespace  
                

            

        else:
            print("if ul is open?",ultag_is_open)
            previouslinespace = 0
            if ultag_is_open == True:
                
                line ="</ul>"+'\n'+line
                ultag_is_open = False
            if  sub_ultag_is_open ==True:
                line ="</ul>"+'\n'+line
                sub_ultag_is_open =False
         
            print("Number of ul tag to be closed" ,count)
            if count >=1:
                
                for i in range(count):
                    ultags ="</ul>"+'\n'
                line +=ultags
                count =0               


        #     if previouslinespace == 0:
        #         previouslinespace = currentlinespace
        #         if ulisopen==False:
        #             ulisopen=True
        #             line= li.sub(r"<ul><li>\2</li>",line)
        #         else:
        #             line= li.sub(r"<li>\2</li>",line)
        #     else:
                
        #         if currentlinespace-previouslinespace==2 or currentlinespace==previouslinespace:
        #             if ulisopen==False:
        #                 ulisopen=True   
        #                 previouslinespace = currentlinespace
        #                 line= li.sub(r"<ul><li>\2</li>",line)
        #             else:
        #                  line= li.sub(r"<li>\2</li>",line)
        #         else:
                    
        #             #line= li.sub(r"</ul>",line)
        #             line= li.sub(r"<ul><li> \2 <li>",line)
        #             ulisopen=True
                
        # else:
        #     print("is ul tag open?",ulisopen)
        #     if ulisopen==True:
        #         ulisopen=False
        #         line+="</ul>"

            #ul =re.compile(r"[ ]{0,3}[*+-]\s+(.*)")
            
            #li = re.compile(r"^(\s*(\-\s|\*\s)([^\r]+?)(?<=$))",re.MULTILINE)
            
    


        #pre 

        #pre = re.compile(r"\s{4,}(\-\s|\*\s)([\w+(\[|\^&+\-.',%\(\/)=!\:>\'\"\s]+?)(?<=$)")
        #line= pre.sub(r"<pre><code>\2</code></pre>",line)
        
        #hr dividing
         
        hr =  re.compile(r"(?:\s*-{3,})+|(?:\s*\*{3,})+|(?:\s*_{3,})+")
        if hr.search(line):
            print("HR",line)
        line=hr.sub(r"<hr>\n", line)

        #Bold
        #bold = re.compile("\*\*[\w+(\[|\^&+\-%\/=!\:>\'\"\])\s+]*\*\*")
        bold = re.compile(r"(\*\*|__)(?=\S)(.+?[*_]*)(?<=\S)\1")
        
        if bold.search(line):
            print("Bold",line)
        line= bold.sub(r"<strong>\2</strong>\n", line)

        #Italic
        italic = re.compile(r"(\*|_)(?=\S)(.+?[*_]*)(?<=\S)\1")
       
        if italic.search(line):
            print("Italic",line)
        line=italic.sub(r"<em>\2</em>\n", line)

        #Strikethrough
        strikethrough = re.compile(r"(~~)(?=\S)(.+?[*_]*)(?<=\S)\1")
        
        if strikethrough.search(line):
            print("Italic",line)
        line=strikethrough.sub(r"<s>\2</s>\n", line)
        
        
        
        
      
        
        
        

        if (heading_matches != None):
            tag = heading_matches.end()
            hashTagLen = heading_matches.end() - 1
            htmlTag = "h" + str(hashTagLen)
            content = line.strip()[(hashTagLen + 1):]
            results += "<" + htmlTag + ">" + content + "</" + htmlTag + ">"+'\n'
        
        
        else:
            print("no heading")
            #if line.isspace() ==False:
            if line.strip() != "":
                if "<ul>" not in line and "</ul>" not in line:
                    if "<li>" not in line and "</li>" not in line:
                        print(" adding <P> tag in line",line)
                        results+="<p>"+line +"</p>"+'\n'

                    else:
                        results+=line +'\n'
                else:
                    results+=line+'\n'
            else:
                results+=line+'\n'
        print("RESULTS after all the edits\n",results)
    return results