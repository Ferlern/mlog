import re
import os
import sys


INPUT_DIRECTORY = './raw'
OUTPUT_DIRECTORY = './compiled'
IMPORT_PATTERN = r'(\s*?)import (.+?)(\(.*){0,1}$'


class MlogFile:
    def __init__(self,
                 full_name: str,
                 path: str) -> None:

        self.full_name = full_name
        self.old_directory_path = path
        self.name, self.ext = self._split_name()
        self.new_directory_path, self.old_path, self.new_path = self._generate_path()
         
        self.content: list[str] = []
        
    def is_mlog(self):
        return self.ext == '.mlog'
        
    def _split_name(self):
        splitted_name = os.path.splitext(self.full_name)
        name = splitted_name[0]
        ext = splitted_name[1]
        return name, ext
    
    def _generate_path(self):
        path = self.old_directory_path
        name = self.full_name
        new_directory_path = path.replace(INPUT_DIRECTORY, OUTPUT_DIRECTORY, 1)
        old_path=f"{path}\\{name}"
        new_path=f"{new_directory_path}\\{name}"
        return new_directory_path, old_path, new_path

class Compiler:
    def __init__(self, input_directory: str, output_directory: str) -> None:
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.files: list[MlogFile] = []
        self.prev_token: str = ""
        self.prev_value: list = []
    
    def compile(self):
        self._read_directory()
        
        for file in self.files:
            self._parse_mlog_file(file)
            
        for file in self.files:
            os.makedirs(file.new_directory_path, exist_ok=True)
            
            with open(file.new_path, 'w') as new_file:
                for line in file.content:
                    new_file.write(line)
    
    def _read_directory(self):
        for path, subfolders, files in os.walk(INPUT_DIRECTORY):
            for file in files:
                
                mlog_file = MlogFile(
                    full_name=file,
                    path=path
                )
                if mlog_file.is_mlog():
                    self.files.append(mlog_file)
                
    def _parse_mlog_file(self, file: MlogFile, intends=0, variables={}):
        print(f"parse file {file.full_name}; variables: {variables}")
        
        if content := file.content:
            imported_content = self._prepaire_content_for_import(content, intends, variables)
            return imported_content
        
        content = []

        with open(file.old_path, 'r') as mlog_file:
            lines = mlog_file.readlines()
            
            for line in lines:
                token, value = self._parse_line(line)
                
                if token == "IMPORT":
                    imported_file = self._find_file(value[1])
                    content.extend(
                        self._parse_mlog_file(
                            imported_file,
                            intends=len(value[0]),
                            variables=value[2]
                        )
                    )
                elif token == "MULTILINE_IMPORT":
                    continue
                else:
                    content.append(value)
        
        file.content = content
        imported_content = self._prepaire_content_for_import(content, intends, variables)
        return imported_content
    
    def _find_file(self, name: str) -> MlogFile:
        for file in self.files:
            if name in [file.name, file.full_name]:
                return file
        print(f"ERROR: can't find file with name {name}")
        sys.exit(1)
        
    def _parse_line(self, line: str):
        if self.prev_token == 'MULTILINE_IMPORT':
            if line.endswith(")"):
                token = "IMPORT"
            else:
                token = "MULTILINE_IMPORT"
            
            prev_value = self.prev_value

            old_variables = prev_value[2]
            new_variables = self._resolve_variable(line.strip())

            variables = old_variables | new_variables
            prev_value[2] = variables

            value = prev_value
        
        elif import_expr := re.search(IMPORT_PATTERN, line):

            if variables_string := import_expr.group(3):
                if variables_string.endswith(")"):
                    token = "IMPORT"
                else:
                    token = "MULTILINE_IMPORT"
                variables = self._resolve_variable(variables_string)
            else:
                token = "IMPORT"
                variables = {}
    
            value = [import_expr.group(1), import_expr.group(2), variables]
        else:
            token = "LINE"
            value = line
        
        self.prev_token = token
        self.prev_value = value
        return token, value
        
    def _resolve_variable(self, variables_string: str):
        variables_string = variables_string.strip("()")
        variables_list = re.split(r',|, ', variables_string)

        variables_dict = {}
        for variable in variables_list:
            
            variable = variable.strip()
            if not len(variable): continue

            key, value = re.split(r' *= *', variable)
            variables_dict[key] = value
            
        return variables_dict
    
    def _prepaire_content_for_import(self, content: list[str], intends: int, variables: dict):
        return [f"{intends*' '}{self._use_varibles(line, variables)}" for line in content]

    
    def _use_varibles(self, line: str, variables: dict) -> str:
        for variable, value in variables.items():
            line = line.replace(variable, value)
            
        return line
            
    
compailer = Compiler(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
compailer.compile()