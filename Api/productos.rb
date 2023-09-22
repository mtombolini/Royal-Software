require 'net/http'
require 'openssl'
require 'json'
require 'rubyXL' # Requiere la gema rubyXL

# Leer el token desde un archivo
file_path = 'token.txt'
token = File.read(file_path).strip

url = 'https://api.bsale.io/v1/product_types.json'
uri = URI.parse(url)
http = Net::HTTP.new(uri.host, uri.port)

# Activa SSL
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

# Crear un nuevo libro de trabajo y añadir una hoja
workbook = RubyXL::Workbook.new
worksheet = workbook[0]
worksheet.add_cell(0, 1, 'SKU')
worksheet.add_cell(0, 2, 'NOMBRE')

row_index = 1

offset = 0
limit = 15 # O el máximo que permita la API

loop do
  new_url = "#{url}?limit=#{limit}&offset=#{offset}"
  new_uri = URI.parse(new_url)
  request = Net::HTTP::Get.new(new_uri.request_uri)

  # Configura cabeceras
  request['Content-Type'] = 'application/json'
  request['access_token'] = token

  # Verifica el token
  puts "Token utilizado: #{token}"

  # Realiza la solicitud y captura la respuesta
  response = http.request(request)

  # Verifica el estado de la respuesta HTTP
  puts "Código de estado HTTP: #{response.code}"

  # Imprime la respuesta en bruto
  puts "Respuesta HTTP en bruto:"
  puts response.body

  begin
    # Intenta parsear la respuesta como JSON
    respuesta = JSON.parse(response.body)
  rescue JSON::ParserError => e
    puts "Error al parsear la respuesta como JSON: #{e.message}"
    break
  end

  # Imprimir toda la respuesta
  puts "Respuesta de la API:"
  p respuesta

  # Romper el bucle si no hay más elementos
  break if respuesta['items'].nil? || respuesta['items'].empty?

  # Actualiza el offset para la siguiente iteración
  offset += limit
end
