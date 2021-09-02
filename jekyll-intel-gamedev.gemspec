# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "jekyll-intel-gamedev"
  spec.version       = "0.1.0"
  spec.authors       = ["Iron Horse"]
  spec.email         = ["logan@ironhorse.io"]

  spec.summary       = "Theme for Github Pages site."
  spec.homepage      = "http://www.gametechdev.github.io"
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_sass|LICENSE|README|_config\.yml)!i) }

  spec.add_runtime_dependency 'jekyll', '4.2.0'
  spec.add_runtime_dependency 'kramdown-parser-gfm', '1.1.0'
  spec.add_runtime_dependency 'jekyll-seo-tag', '2.7.1'
  spec.add_runtime_dependency 'jekyll-autoprefixer', '1.0.1'
end
