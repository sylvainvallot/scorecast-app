export type Team = {
  id: string;
  name: string;
  color: {
    primary: string;
    secondary: string;
  };
  city: string;
  subteams?: string[];
};
