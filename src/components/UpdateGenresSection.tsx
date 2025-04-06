
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';

const genres = [
  { id: 1, name: 'Motivation', selected: true },
  { id: 2, name: 'Psychology', selected: true },
  { id: 3, name: 'Spirituality', selected: true },
  { id: 4, name: 'Productivity', selected: false },
  { id: 5, name: 'Cybersecurity Awareness', selected: false },
  { id: 6, name: 'Mindfulness & Meditation', selected: false },
  { id: 7, name: 'Positive Thinking', selected: false },
  { id: 8, name: 'Success Stories', selected: false },
  { id: 9, name: 'Adventure & Exploration', selected: false },
  { id: 10, name: 'Overcoming Adversity', selected: false },
  { id: 11, name: 'Neuroscience', selected: false },
  { id: 12, name: 'Cognitive Science', selected: false },
  { id: 13, name: 'Human-Computer Interaction', selected: false },
  { id: 14, name: 'Philosophy', selected: false },
  { id: 15, name: 'Goal Setting & Achievement', selected: false },
  { id: 16, name: 'Resilience & Grit', selected: false },
  { id: 17, name: 'Creativity', selected: false },
  { id: 18, name: 'Travel', selected: false },
];

const UpdateGenresSection = () => {
  const [selectedGenres, setSelectedGenres] = useState(genres);

  const toggleGenre = (id: number) => {
    setSelectedGenres(
      selectedGenres.map(genre => 
        genre.id === id ? { ...genre, selected: !genre.selected } : genre
      )
    );
  };

  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {selectedGenres.map(genre => (
          <button
            key={genre.id}
            onClick={() => toggleGenre(genre.id)}
            className={`px-4 py-1 text-sm rounded-full border ${
              genre.selected
                ? 'border-red-500 text-red-600 bg-white'
                : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
            }`}
          >
            {genre.name}
          </button>
        ))}
      </div>
      
      <Button variant="destructive" className="mt-8 px-4">
        Save Changes
      </Button>
    </div>
  );
};

export default UpdateGenresSection;
