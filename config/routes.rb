Rails.application.routes.draw do
  get 'home', to: 'home#index'
  get 'performers', to: 'performers#index'
  get 'unhealthy/:id', to: 'unhealthy#show', as: 'unhealthy_show'
  get 'healthy', to: 'healthy#index'
  resources :unhealthy, only: [:index, :show]
  get '/unhealthy/video/:filename', to: 'unhealthy#video', as: 'unhealthy_video'
  resources :inputs, only: [:index, :create]
  root 'home#index'
  get 'input/index', to: 'inputs#index', as: 'input_index'
end
