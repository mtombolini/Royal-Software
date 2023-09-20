require 'net/http'
require 'openssl'
require 'json'
require 'rubyXL' # Requiere la gema rubyXL

# Leer el token desde un archivo
file_path = 'token.txt'
token = File.read(file_path).strip

url = 'https://api.bsale.cl/v1/clients.json'
uri = URI.parse(url)
http = Net::HTTP.new(uri.host, uri.port)

# Activa SSL
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

# Crear un nuevo libro de trabajo y añadir una hoja
workbook = RubyXL::Workbook.new
worksheet = workbook[0]
worksheet.add_cell(0, 0, 'Nombre')
worksheet.add_cell(0, 1, 'RUT')

row_index = 1

offset = 0
limit = 15 # O el máximo que permita la API

loop do
  new_url = "#{url}?limit=#{limit}&offset=#{offset}"
  new_uri = URI.parse(new_url)
  request = Net::HTTP::Get.new(new_uri.request_uri)

  # Configura cabeceras
  request['Content-Type'] = 'application/json'
  request['access_token'] = token # Usar el token leído del archivo

  response = http.request(request)
  respuesta = JSON.parse(response.body)

  # Romper el ciclo si no hay más elementos
  break if respuesta['items'].nil? || respuesta['items'].empty?

  # Añadir nombres y RUT de los clientes al archivo Excel
  respuesta['items'].each do |client|
    worksheet.add_cell(row_index, 0, client['firstName'])
    worksheet.add_cell(row_index, 1, client['code']) # Asumiendo que 'rut' es la clave para el RUT
    row_index += 1
  end

  # Aumentar el offset para la siguiente iteración
  offset += limit
end

# Guardar el archivo Excel
workbook.write("clientes.xlsx")
