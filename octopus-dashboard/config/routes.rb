Rails.application.routes.draw do
  resources :players do
    collection do
      get 'compare'
      get 'load_suggestions'
    end
  end

  get 'coming', to: 'main#coming'
  get 'compare', to: 'main#compare'

  root to: 'main#coming'

  resources :libraries
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
