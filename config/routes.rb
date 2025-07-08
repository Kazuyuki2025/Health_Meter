Rails.application.routes.draw do
  root 'home#index'
  get 'home', to: 'home#index'
  get 'unhealthy/:id', to: 'unhealthy#show', as: 'unhealthy_show'
  get 'healthy', to: 'healthy#index'
  resources :unhealthy, only: [:index, :show]
  get '/unhealthy/video/:filename', to: 'unhealthy#video', as: 'unhealthy_video'
  get 'input/index', to: 'inputs#index', as: 'input_index'
  resources :inputs
  resources :performers
  resources :performances, only: [:create]
end
